'use strict';

var fs = require('fs');
var colorgram = require('colorgram');
var getPixels = require('get-pixels');

var NUM_COLORS = 12;

function saveColors(colors, outPath) {
    var s = JSON.stringify(colors, undefined, 4);
    fs.writeFileSync(outPath, s);
}

function main() {
    if (process.argv.length != 4) {
        console.log("Usage: generate_control_data.js <image path> <output path>");
        console.log("Example: generate_control_data.js test.jpg test.json");
        return;
    }

    var inPath = process.argv[2];
    var outPath = process.argv[3];

    console.log("Loading image...");
    getPixels(inPath, function(err, pixels) {
        if (err) {
            console.log("Could not load image from '" + inPath + "'.");
            console.log("Please double check that it exists. And, uh, in that location.");
            return;
        }
        var image = {
            'data': pixels.data,
            'width': pixels.shape[0],
            'height': pixels.shape[1],
            'channels': pixels.shape[2]
        };
        console.log("Extracting colors...");
        var colors = colorgram.extract(image, NUM_COLORS);
        console.log("Saving output to '" + outPath + "'...");
        saveColors(colors, outPath);
        console.log("Done.");
    });
}

main();
