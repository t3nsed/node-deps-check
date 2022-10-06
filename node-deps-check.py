import os
import sys
import json

output = 'node-deps-verbose.json'
traverseDir = os.getcwd()
data = {}

if len(sys.argv) > 1:
    traverseDir = sys.argv[1]

for root, dirs, files in os.walk(traverseDir):
    # check only top level dependencies
    # if 'node_modules' not in root:
    for file in files:
        if file == 'package.json':
            print(os.path.join(root, file))
            with open(os.path.join(root, file)) as out:
                try:
                    packageJson = json.load(out)
                except json.decoder.JSONDecodeError:
                    continue
                data[root] = {"version": packageJson.get('version', "no version specified"), "license": packageJson.get('license', "no license"), "dependencies": {
                    "dependencies": packageJson.get('dependencies', "no dependencies"), "devDependencies": packageJson.get('devDependencies', "no dev-dependencies")}}


with open(output, 'w') as out:
    out.write(json.dumps(data))
print('wrote to ', output)
print("run 'npm install' beforehand to get a full list, otherwise only top-level packages will be analyzed.")
