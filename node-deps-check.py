import collections
import os
import sys
import json

loc_output = 'node-deps-verbose.json'
loc_license_sums = 'node-deps-licenses.json'


def format_json_package(package_json, licenses=None):
    """extracts name, license, dependencies from provided package.json file, appends licenses for optional counting"""
    version = package_json.get('version', "no version specified")
    license = package_json.get('license', "no license")
    if licenses is not None:
        licenses.append(str(license))
    dependencies = package_json.get('dependencies', "no dependencies")
    dev_dependendencies = package_json.get(
        'devDependencies', "no dev-dependencies")
    return {"version": version, "license": license, "dependencies": {
        "dependencies": dependencies, "devDependencies": dev_dependendencies}}


def traverse(path: str):
    """Traverse all subdirectories of a given path"""
    data = {}
    licenses = []
    for root, dirs, files in os.walk(path):
        # check only top level dependencies
        # if 'node_modules' not in root:
        for file in files:
            if file == 'package.json':
                with open(os.path.join(root, file)) as out:
                    try:
                        data[root] = format_json_package(json.load(out))
                    except json.decoder.JSONDecodeError:
                        print("could not include ", os.path.join(
                            root, file), " malformed JSON")
                        continue
    license_sums = collections.Counter(licenses)
    return (data, license_sums)


def write_json_to_file(path: str, data):
    with open(path, 'w') as out:
        out.write(json.dumps(data))


traverseDir = os.getcwd()
if len(sys.argv) > 1:
    traverseDir = sys.argv[1]


(data, license_sums) = traverse(traverseDir)

print('----')
write_json_to_file(loc_output, data)
print('wrote results to ', loc_output)
write_json_to_file(loc_license_sums, license_sums)
print('wrote license counts to ', loc_license_sums)
print("run 'npm install' beforehand to get a full list, otherwise only top-level packages will be analyzed.")
