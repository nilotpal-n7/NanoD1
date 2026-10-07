import sys
import os
import subprocess
import argparse

def get_image_dimensions(image_path):
    try:
        # Call ImageMagick to get width and height
        result = subprocess.run(['magick', 'identify', '-format', '%w %h', image_path], 
                                capture_output=True, text=True, check=True)
        parts = result.stdout.strip().split()
        return int(parts[0]), int(parts[1])
    except Exception as e:
        print(f"Error getting image info (is ImageMagick installed?): {e}")
        sys.exit(1)

def convert_to_bmp(input_path, temp_bmp_path, mode='photo', clean=False, auto=False, invert=False):
    print(f"Analyzing {input_path}...")
    w, h = get_image_dimensions(input_path)
    
    cmd = ['magick', input_path]
    
    # If portrait, rotate 90 degrees so it fills the landscape board better
    if w < h:
        print(f"Image is portrait ({w}x{h}). Rotating 90 degrees to fit board.")
        cmd.extend(['-rotate', '90'])
    else:
        print(f"Image is landscape ({w}x{h}).")
        
    if auto:
        print("Applying auto-levels and normalization...")
        cmd.extend(['-auto-level', '-normalize'])
        
    if clean:
        print("Applying noise reduction to remove clutter...")
        cmd.extend(['-despeckle', '-enhance'])

    cmd.extend([
        '-resize', '1056x608^', 
        '-gravity', 'center', 
        '-extent', '1056x608', 
        '-colorspace', 'Gray'
    ])
    
    if invert:
        print("Inverting colors...")
        cmd.extend(['-negate'])
    
    # Mode specific processing
    if mode == 'logo':
        print("Mode: LOGO (Hard thresholding for clean lines, no dithering)")
        # For logos/text: use a threshold to make solid black/white edges without dots
        cmd.extend(['-threshold', '50%'])
    else:
        print("Mode: PHOTO (Floyd-Steinberg dithering for gradients)")
        # For photos: use unsharp, gamma, and dithering
        cmd.extend(['-unsharp', '0x1+0.5+0.05', '-gamma', '1.4', '-dither', 'FloydSteinberg'])
        
    cmd.extend(['-monochrome', f'BMP3:{temp_bmp_path}'])
    
    print("Converting image to 1-bit high quality BMP...")
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"ImageMagick conversion failed: {e}")
        sys.exit(1)

def generate_pas(bmp_path, out_path, min_tw=0.15):
    print("Generating Altium script...")
    with open(bmp_path, 'rb') as f:
        data = f.read()

    if data[:2] != b'BM':
        print("Error: The temporary BMP file is invalid.")
        return

    offset = int.from_bytes(data[10:14], 'little')
    width = int.from_bytes(data[18:22], 'little')
    height = int.from_bytes(data[22:26], 'little', signed=True)
    bpp = int.from_bytes(data[28:30], 'little')

    if bpp != 1:
        print("Error: Temporary BMP is not 1-bit.")
        return

    top_down = False
    if height < 0:
        top_down = True
        height = -height

    pal_offset = 14 + int.from_bytes(data[14:18], 'little')
    c0 = sum(data[pal_offset:pal_offset+3])
    c1 = sum(data[pal_offset+4:pal_offset+7])
    white_val = 1 if c1 > c0 else 0

    row_bytes = (width + 7) // 8
    pad_row_bytes = ((row_bytes + 3) // 4) * 4

    px_mm = 66.0 / width
    half_w = 66.0 / 2.0
    half_h = (height * px_mm) / 2.0

    lines = []
    lines.append("{ =============================================================")
    lines.append("  NanoD1.pas - Generated logo script")
    lines.append("  ============================================================= }")
    lines.append("Const")
    lines.append("    CX      = 33.0;")
    lines.append("    CY      = 19.0;")
    lines.append("    ROT_DEG = -90.0;")
    lines.append("    MIRROR  = 0;")
    lines.append(f"    TW      = {max(px_mm, min_tw):.4f};")
    lines.append("    SIDE    = 1; { 0=Top, 1=Bottom }")
    lines.append("    SCALE   = 0.3;")
    lines.append("Var")
    lines.append("    Board : IPCB_Board;")
    lines.append("    nAdd  : Integer;")
    lines.append("    ca, sa : Real;")
    lines.append("    doMirror : Boolean;")
    lines.append("Procedure L(X1, Y1, X2, Y2 : Real);")
    lines.append("Var T : IPCB_Track; ax, ay, bx, by, rx, ry, qx, qy : Real;")
    lines.append("Begin")
    lines.append("    ax := X1 * SCALE; ay := Y1 * SCALE; bx := X2 * SCALE; by := Y2 * SCALE;")
    lines.append("    If doMirror Then Begin ax := -ax; bx := -bx; End;")
    lines.append("    rx := ax * ca - ay * sa; ry := ax * sa + ay * ca;")
    lines.append("    qx := bx * ca - by * sa; qy := bx * sa + by * ca;")
    lines.append("    T := PCBServer.PCBObjectFactory(eTrackObject, eNoDimension, eCreate_Default);")
    lines.append("    If T = Nil Then Exit;")
    lines.append("    T.X1 := Board.XOrigin + MMsToCoord(CX + rx); T.Y1 := Board.YOrigin + MMsToCoord(CY + ry);")
    lines.append("    T.X2 := Board.XOrigin + MMsToCoord(CX + qx); T.Y2 := Board.YOrigin + MMsToCoord(CY + qy);")
    lines.append("    T.Width := MMsToCoord(TW * SCALE);")
    lines.append("    If SIDE = 1 Then T.Layer := eBottomOverlay Else T.Layer := eTopOverlay;")
    lines.append("    Board.AddPCBObject(T); nAdd := nAdd + 1;")
    lines.append("End;")
    lines.append("Procedure NanoD1;")
    lines.append("Begin")
    lines.append("    nAdd := 0;")
    lines.append("    Board := PCBServer.GetCurrentPCBBoard;")
    lines.append("    If Board = Nil Then Exit;")
    lines.append("    If SIDE = 1 Then doMirror := (MIRROR = 0) Else doMirror := (MIRROR = 1);")
    lines.append("    ca := Cos(ROT_DEG * 3.14159265 / 180.0); sa := Sin(ROT_DEG * 3.14159265 / 180.0);")
    lines.append("    PCBServer.PreProcess;")
    
    track_count = 0
    for row in range(height):
        y = (height - 1 - row) * px_mm - half_h if top_down else row * px_mm - half_h
        
        in_run = False
        run_start = 0
        
        for col in range(width):
            byte_idx = col // 8
            bit_idx = 7 - (col % 8)
            byte_pos = offset + row * pad_row_bytes + byte_idx
            pixel = (data[byte_pos] >> bit_idx) & 1
            
            if pixel == white_val:
                if not in_run:
                    in_run = True
                    run_start = col
            
            if (pixel != white_val or col == width - 1) and in_run:
                x1 = run_start * px_mm - half_w
                x2 = (col + 1) * px_mm - half_w if pixel == white_val and col == width - 1 else col * px_mm - half_w
                lines.append(f"    L({x1:.4f},{y:.4f},{x2:.4f},{y:.4f});")
                track_count += 1
                in_run = False

    lines.append("    PCBServer.PostProcess;")
    lines.append("    Board.ViewManager_FullUpdate;")
    lines.append("    Client.SendMessage('PCB:Zoom', 'Action=Redraw', 255, Client.CurrentView);")
    lines.append(f"    ShowMessage('Done! Tracks: ' + IntToStr(nAdd));")
    lines.append("End;")
    
    with open(out_path, 'w') as f:
        f.write('\n'.join(lines))
        
    print(f"SUCCESS: Generated {out_path} with {track_count} tracks.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Automated Altium Logo Script Generator')
    parser.add_argument('image', help='Input image file (JPG, PNG, BMP, etc)')
    parser.add_argument('--invert', action='store_true', help='Invert colors (1->0, 0->1)')
    parser.add_argument('--out', default='NanoD1.pas', help='Output pas file (default: NanoD1.pas)')
    parser.add_argument('--mode', choices=['photo', 'logo'], default='photo', help="Use 'photo' for dithering gradients, or 'logo' for clean solid lines without dots (removes clutter)")
    parser.add_argument('--clean', action='store_true', help='Apply despeckle to remove small noise and clutter')
    parser.add_argument('--auto', action='store_true', help='Automatically fix contrast and levels before processing')
    parser.add_argument('--tw', type=float, default=0.15, help='Minimum track width in mm (default: 0.15, JLCPCB minimum for silkscreen)')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.image):
        print(f"Error: File '{args.image}' not found.")
        sys.exit(1)
        
    # Create a preview BMP path based on the input image name
    base_name = os.path.splitext(os.path.basename(args.image))[0]
    preview_bmp = f"{base_name}.bmp"
    
    # Step 1: Automatically format and convert the image
    convert_to_bmp(args.image, preview_bmp, mode=args.mode, clean=args.clean, auto=args.auto, invert=args.invert)
    
    # Step 2: Read the BMP and spit out the Altium Script
    generate_pas(preview_bmp, args.out, min_tw=args.tw)
    
    print(f"Saved preview image as: {preview_bmp}")
