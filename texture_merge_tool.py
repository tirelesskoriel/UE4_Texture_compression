import sys
import os
from PIL import Image

AO_FLAG = "_ao.jpg"
DISPLACEMENT_FLAG = "_displacement.jpg"
ROUGHNESS_FLAG = "_roughness.jpg"
NORMAL_FLAG = "_normal.jpg"
CAVITY_FLAG = "_cavity.jpg"
ALBEDO_FLAG = "_albedo.jpg"

def getPath(flags, root, f_names):
    paths = {}
    for name in f_names:
        f_path = os.path.abspath(os.path.join(root, name))
        for flag in flags:
            if name.lower().rfind(flag) >= 0:
                paths[flag] = f_path
                break
    return paths

def merge_high(root, f_names):

    flags = [AO_FLAG, DISPLACEMENT_FLAG, ROUGHNESS_FLAG, NORMAL_FLAG, CAVITY_FLAG, ALBEDO_FLAG]
    paths = getPath(flags, root, f_names)

    if len(flags) != len(paths):
        print(paths)
        return

    ao_path = paths[AO_FLAG]
    displacement_path = paths[DISPLACEMENT_FLAG]
    roughness_path = paths[ROUGHNESS_FLAG]
    normal_path = paths[NORMAL_FLAG]
    cavity_path = paths[CAVITY_FLAG]
    albedo_path = paths[ALBEDO_FLAG]

    albedo = Image.open(albedo_path)
    r, g, b = albedo.split()

    roughness = Image.open(roughness_path)
    ar_target_path = os.path.join(root, "ar.png")

    Image.merge("RGBA", (r, g, b, roughness.getchannel(0))).save(ar_target_path)

    albedo.close()
    roughness.close()

    normal = Image.open(normal_path)

    canvity = Image.open(cavity_path)
    canvity_pix = canvity.load()

    AO = Image.open(ao_path)
    ao_pix = AO.load()
    
    size = AO.size[0]

    for x in range(size - 1):
        for y in range(size - 1):
            result = int(ao_pix[x, y][0] * canvity_pix[x, y][0] / 255)
            AO.putpixel((x, y), (result, result, result))
    
    displacement = Image.open(displacement_path)

    r = normal.getchannel(0)
    g = normal.getchannel(1)
    b = AO.getchannel(0)
    a = displacement.getchannel(0)

    naob_target_path = os.path.join(root, "naob.png")
    Image.merge("RGBA", (r, g, b, a)).save(naob_target_path)

    normal.close()
    AO.close()
    displacement.close()
    canvity.close()

def merge_simple(root, f_names):

    flags = [AO_FLAG, DISPLACEMENT_FLAG, ROUGHNESS_FLAG]
    paths = getPath(flags, root, f_names)

    if len(flags) != len(paths):
        print(paths)
        return

    ao_path = paths[AO_FLAG]
    dis_path = paths[DISPLACEMENT_FLAG]
    r_path = paths[ROUGHNESS_FLAG]
        
    AO = Image.open(ao_path)
    displacement = Image.open(dis_path)
    roughness = Image.open(r_path)

    c_ao = AO.getchannel(0)
    c_d = displacement.getchannel(0)
    c_r = roughness.getchannel(0)

    target_path = os.path.join(root, "aodr.jpg")
    Image.merge("RGB", (c_ao, c_d, c_r)).save(target_path)

    AO.close()
    displacement.close()
    roughness.close()
    

def main():
    if (len(sys.argv) > 1):

        space_path = "."
        if (len(sys.argv) > 2):
            space_path = sys.argv[2]

        for root,dirs,files in os.walk(space_path):
            print(root, dirs, files)
            if len(files) == 0:
                continue

            match sys.argv[1]:
                case "simple":
                    merge_simple(root, files)
                case "high":
                    merge_high(root, files)

main()