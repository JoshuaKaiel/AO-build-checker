import sys
from math import ceil
from pathlib import Path
import pandas as pd
from ast import literal_eval

def validate_savant(ratio1, ratio2, ratio3):
    ratios = [ratio1, ratio2, ratio3]
    ratios.sort(reverse=True)
    return ratios[0] < 0.5 and ratios[1] < 0.4 and ratios[2] < 0.4

def calc_usable(strength, spirit, weapons, magic):
    df = pd.read_csv(Path(".") / "skill_list.csv", delimiter=";")

    # Get the learnable skills
    skill_list = []
    for index, row in df.iterrows():
        
        name = row["name"] # Name of the skill
        exclusive = " (exclusive to " + row["exclusive"] + ")" if not pd.isna(row["exclusive"]) else "" # add the exclusiveness if it exists

        stats =literal_eval(row["stats"]) # Common use stats
        aux_stats = literal_eval(row["shared"]) # Can use stats (for weapon/strength builds)
        reqs = int(row["requirements"]) / len(stats) # Point requirements
        aux_reqs = int(row["requirements"]) / (len(stats) + len(aux_stats)) # Auxiliar point requirements (for weapon/strength builds)

        level_calc = "spi" in stats or "wep" in stats # Take in account spirit and weapon level variations, or not

        # Change stat names to stat values
        st_values = []
        aux_st_values = []

        for elem in stats:
            match elem:
                case "str":
                    st_values.append(strength)
                    aux_st_values.append(strength)
                case "spi":
                    st_values.append(spirit)
                    aux_st_values.append(spirit)
                case "wep":
                    st_values.append(weapons)
                    aux_st_values.append(weapons)
                case "mag":
                    st_values.append(magic)
                    aux_st_values.append(magic)

        for elem in aux_stats:
            match elem:
                case "str":
                    aux_st_values.append(strength)
                case "spi":
                    aux_st_values.append(spirit)
                case "wep":
                    aux_st_values.append(weapons)
                case "mag":
                    aux_st_values.append(magic)

        # If needs item level calculation
        if level_calc:

            # But is unique, and satisifies the requirements
            if row["unique"] and (all(elem > reqs for elem in st_values) or all(elem > aux_reqs for elem in aux_st_values)):
                skill_string = name + exclusive
                skill_list.append(skill_string)

            # and we need to determine the max weapon level
            else:
                actual_req = (min(st_values) - (reqs - (30 / len(st_values)))) / 2
                actual_aux_req = (min(aux_st_values) - (aux_reqs - (30 / len(aux_st_values)))) / 2
                max_wep_level = int(ceil(max([elem for elem in [actual_req, actual_aux_req]])))

                # print(row)
                # print(f"Normal: {actual_req} -- {st_values} | {reqs}")
                # print(f"Auxiliar: {actual_aux_req} -- {aux_st_values} | {aux_reqs}")
                # print(f"Final: {max_wep_level}")

                if max_wep_level >= 0:
                    skill_string = f"{name} for an item of level {max_wep_level}" + exclusive
                    skill_list.append(skill_string)

        # else the stats just need to be bigger than the requirements
        else:
            if all(elem > reqs for elem in st_values) or all(elem > aux_reqs for elem in aux_st_values):
                skill_string = name + exclusive
                skill_list.append(skill_string)
    
    return skill_list

def main():
    try: 
        # Initialization, in case one is ommited on file input
        strength = 0
        spirit = 0
        weapons = 0
        magic = 0

        # Locate command line arguments
        has_args = len(sys.argv) > 1
        do_output = -1
        do_input = -1
        
        if has_args:
            try:
                do_input = sys.argv.index("-i")
            except Exception:
                ...
            
            try:
                do_output = sys.argv.index("-o")
            except Exception:
                ...

        # Read from file
        if has_args and do_input != -1:
            file = Path(".") / sys.argv[do_input + 1]
            fcontent = file.open().read().split(" ")
            for i in range(0, len(fcontent), 2):
                match fcontent[i]:
                    case "str":
                        strength = int(fcontent[i + 1])
                    case "spi":
                        spirit = int(fcontent[i + 1])
                    case "wep":
                        weapons = int(fcontent[i + 1])
                    case "mag":
                        magic = int(fcontent[i + 1])
        # Ask for input
        else :
            print("Input the stats allocated in strength:") 
            strength = int(input())
            print("Input the stats allocated in spirit:") 
            spirit = int(input())
            print("Input the stats allocated in weapons:") 
            weapons = int(input())
            print("Input the stats allocated in magic:") 
            magic = int(input())
            
        # Run calculations
        total = strength + spirit + weapons + magic

        str_ratio = strength / total
        spi_ratio = spirit / total
        wep_ratio = weapons / total
        mag_ratio = magic / total

        build_name = ""
        
        if str_ratio >= 0.6:
            print(f"With {strength} strength over {total} points, your build is a Berserker.")
            build_name = "Berserker"
        elif spi_ratio >= 0.6:
            print(f"With {spirit} spirit over {total} points, your build is an Oracle.")
            build_name = "Oracle"
        elif wep_ratio >= 0.6:
            print(f"With {weapons} weapons over {total} points, your build is a Warrior.")
            build_name = "Warrior"
        elif mag_ratio >= 0.6:
            print(f"With {magic} magic over {total} points, your build is a Mage.")
            build_name = "Mage"
        elif str_ratio >= 0.4 and spi_ratio >= 0.4:
            print(f"With {strength} strength and {spirit} spirit over {total} points, your build is a Juggernaut.")
            build_name = "Juggernaut"
        elif str_ratio >= 0.4 and wep_ratio >= 0.4:
            print(f"With {strength} strength and {weapons} weapons over {total} points, your build is a Warlord.")
            build_name = "Warlord"
        elif str_ratio >= 0.4 and mag_ratio >= 0.4:
            print(f"With {strength} strength and {magic} magic over {total} points, your build is a Warlock.")
            build_name = "Warlock"
        elif spi_ratio >= 0.4 and wep_ratio >= 0.4:
            print(f"With {spirit} spirit and {weapons} weapons over {total} points, your build is a Knight.")
            build_name = "Knight"
        elif spi_ratio >= 0.4 and mag_ratio >= 0.4:
            print(f"With {spirit} spirit and {magic} magic over {total} points, your build is a Paladin.")
            build_name = "Paladin"
        elif wep_ratio >= 0.4 and mag_ratio >= 0.4:
            print(f"With {weapons} weapons and {magic} magic over {total} points, your build is a Conjurer.")
            build_name = "Conjurer"
        elif str_ratio >= 0.15 and spi_ratio >= 0.15 and wep_ratio >= 0.15 and validate_savant(str_ratio, spi_ratio, wep_ratio):
            print(f"With {strength} strength, {spirit} spirit and {weapons} weapons over {total} points, your build is a Savant.")
            build_name = "Savant (Str/Spi/Wep)"
        elif str_ratio >= 0.15 and spi_ratio >= 0.15 and mag_ratio >= 0.15 and validate_savant(str_ratio, spi_ratio, mag_ratio):
            print(f"With {strength} strength, {spirit} spirit and {magic} magic over {total} points, your build is a Savant.")
            build_name = "Savant (Str/Spi/Mag)"
        elif str_ratio >= 0.15 and wep_ratio >= 0.15 and mag_ratio >= 0.15 and validate_savant(str_ratio, wep_ratio, mag_ratio):
            print(f"With {strength} strength, {weapons} weapons and {magic} magic over {total} points, your build is a Savant.")
            build_name = "Savant (Str/Wep/Mag)"
        elif spi_ratio >= 0.15 and wep_ratio >= 0.15 and mag_ratio >= 0.15 and validate_savant(spi_ratio, wep_ratio, mag_ratio):
            print(f"With {spirit} spirit, {weapons} weapons and {magic} magic over {total} points, your build is a Savant.")
            build_name = "Savant (Spi/Wep/Mag)"
        else:
            ratios = [str_ratio, spi_ratio, wep_ratio, mag_ratio]
            ratios.sort(reverse=True)

            if validate_savant(ratios[0], ratios[1], ratios[2]):
                print(f"With {strength} strength, {spirit} spirit, {weapons} weapons and {magic} magic over {total} points, your build is a Savant, despite not having three stats over 15%.")
                build_name = "Savant"
            else:
                print(f"Your build shouldn't exist, have it checked.")

        str_percent = round(str_ratio*100, 2)
        spi_percent = round(spi_ratio*100, 2)
        wep_percent = round(wep_ratio*100, 2)
        mag_percent = round(mag_ratio*100, 2)

        print(f"\nStat percentages: {str_percent}% strength, {spi_percent}% spirit, {wep_percent}% weapons, {mag_percent}% magic")

        skills = calc_usable(strength, spirit, weapons, magic)
        print(f"\nUsable skills:")
        for skill in skills:
            print(f"\n\t{skill}")


        # Save to textfile
        if has_args and do_output != -1:
            file = Path(".") / sys.argv[do_output + 1]
            fd = file.open("w")

            fd.write(f"""{build_name}\n\n"""
                     """Spread:"""
                     f"""\n\t{strength} ({str_percent}%) strength"""
                     f"""\n\t{spirit} ({spi_percent}%) spirit"""
                     f"""\n\t{weapons} ({wep_percent}%) weapons"""
                     f"""\n\t{magic} ({mag_percent}%) magic""")
            
            fd.write("\n\nUsable skills:")
            for skill in skills:
                fd.write(f"\n\t{skill}")

            fd.close()
                    
    except Exception as e:
        print(f"Something went wrong: {e}")

if __name__ == "__main__":
    main()