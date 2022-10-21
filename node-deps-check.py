import collections, os, sys, json
from operator import contains

output = 'node-deps-verbose.json'
outputLicenseSums = 'node-deps-licenses.json'
traverseDir = os.getcwd()
data = {}
licenseSums = []
nonPermissive = ['GPL-3.0']

if len(sys.argv) > 1:
    traverseDir = sys.argv[1]

for root, dirs, files in os.walk(traverseDir):
    # check only top level dependencies
    # if 'node_modules' not in root:
    for file in files:
        if file == 'package.json':
            with open(os.path.join(root, file)) as out:
                try:
                    packageJson = json.load(out)
                except json.decoder.JSONDecodeError:
                    print("could not include ", os.path.join(
                        root, file), " malformed JSON")
                    continue
                version = packageJson.get('version', "no version specified")
                license = packageJson.get('license', "no license")
                if license in nonPermissive:
                    print("Warning: ", root, " contains the license ", license)
                licenseSums.append(str(license))
                dependencies = packageJson.get(
                    'dependencies', "no dependencies")
                devDependencies = packageJson.get(
                    'devDependencies', "no dev-dependencies")

                data[root] = {"version": version, "license": license, "dependencies": {
                    "dependencies": dependencies, "devDependencies": devDependencies}}


licenseSums = collections.Counter(licenseSums)

with open(outputLicenseSums, 'w') as out:
    out.write(json.dumps(licenseSums))

with open(output, 'w') as out:
    out.write(json.dumps(data))
print('----')
print('wrote results to ', output)
print('wrote license counts to ', outputLicenseSums)
print("run 'npm install' beforehand to get a full list, otherwise only top-level packages will be analyzed.")
