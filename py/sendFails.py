import helpers
import json

config = helpers.getConfig()

# Pick up the ping results directory from the dictionary we created above
# and use it to go get all the ping result files in that directory
files = helpers.getFileList()
for file in files:
    with open(file, 'r') as infile:
        try:
            # Extract the json as json dictionary/object from the file
            output = json.load(infile)
            print(output)
            if helpers.sendOutputToAPI(output):
                # Delete the file
                # os.remove(file)
                print("Sent ok, delete")
        except Exception as e:
            print("Error processing: ", file)
            print(e)
