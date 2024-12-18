/*
###########################################################################################
Supplementary Document 1
Author: Revanth Mamidala 
Inspired from the script of Daniel Paluba Daily_aggregates_GEE (palubad@natur.cuni.cz).
(contact: mrevanth@iastate.edu)
Expaination: The below script can be executed in Google Earth Engine to extract rainfall data
at 22 rain gauge locations in rainGaugeSHP shapefile. The script has to be uncommented at 
lines 76-85 so that the webpage does not crash.
###########################################################################################
*/

//Raingauge shapefile datasets
var rainGaugeSHP = ee.FeatureCollection("projects/ee-revanthm81011/assets/StudyArea_RainGauges");

// Set start and end dates
var startDate = '2016-01-01'; //'2006-01-01'
var endDate = '2024-11-01'; // '2016-01-01'

// Load the datasets
var ERA5_Land = ee.ImageCollection("ECMWF/ERA5_LAND/HOURLY").select('total_precipitation_hourly')
              .filterDate(startDate, endDate);

var CHIRPS = ee.ImageCollection("UCSB-CHG/CHIRPS/DAILY").select('precipitation')
              .filterDate(startDate, endDate);

var PERSIANN = ee.ImageCollection('NOAA/PERSIANN-CDR').select('precipitation')
              .filterDate(startDate, endDate);

var GPM = ee.ImageCollection('NASA/GPM_L3/IMERG_V07').select('precipitation')
              .filterDate(startDate, endDate);

var GSMAP = ee.ImageCollection('JAXA/GPM_L3/GSMaP/v8/operational')
              .filterDate(startDate, endDate).select('hourlyPrecipRate');

var GLDAS = ee.ImageCollection('NASA/GLDAS/V021/NOAH/G025/T3H')
              .filterDate(startDate, endDate).select('Rainf_f_tavg');

// New datasets
var ERA5_daily = ee.ImageCollection('ECMWF/ERA5_LAND/DAILY_AGGR').select('total_precipitation_sum')
                  .filterDate(startDate, endDate);

var PRISM = ee.ImageCollection('OREGONSTATE/PRISM/AN81d').select('ppt')
                  .filterDate(startDate, endDate);

// Function to generate daily precipitation data
var addweatherData = function(img) {
    var date = img.get('system:time_start');

    var currentDate_daily = ee.Date(date).format();
    var nextDay_daily = ee.Date(ee.Number.parse(date).add(86399999)).format();

    // Process each dataset
    var precipitationCHIRPS = CHIRPS.filterDate(currentDate_daily, nextDay_daily).first()
                  .rename('precipitationCHIRPS');

    var precipitationERA5_daily = ERA5_daily.filterDate(currentDate_daily, nextDay_daily).first()
                  .rename('precipitationERA5_daily');

    var precipitationPRISM = PRISM.filterDate(currentDate_daily, nextDay_daily).first()
                  .rename('precipitationPRISM');

    var precipitationPERSIANN = PERSIANN.filter(ee.Filter.date(currentDate_daily, nextDay_daily)).first()
                  .rename('precipitationPERSIANN');

    var precipitationGPM = GPM.filter(ee.Filter.date(currentDate_daily, nextDay_daily)).reduce(ee.Reducer.sum(), 16)
                  .rename('precipitationGPM');

    var precipitationGSMAP = GSMAP.filter(ee.Filter.date(currentDate_daily, nextDay_daily)).reduce(ee.Reducer.sum(), 16)
                  .rename('precipitationGSMAP');

    var precipitationGLDAS = GLDAS.filter(ee.Filter.date(currentDate_daily, nextDay_daily)).reduce(ee.Reducer.sum(), 16)
                  .multiply(10800) // from kg/m²/s to mm
                  .rename('precipitationGLDAS');

    // Select datasets for analysis
    var selected_datasets = [
        // Uncomment to add more datasets
         precipitationCHIRPS,
        // precipitationERA5_daily,
        // precipitationPRISM,
        // precipitationPERSIANN, // 2005 - 2020 only
        // precipitationGPM,
        // precipitationGSMAP,
        // precipitationGLDAS
    ];

    return img.rename('precipitationCHIRPS').addBands(selected_datasets)
                                            .setMulti({currentDate: currentDate_daily});
};

// Map the function across CHIRPS dataset
var dataset = CHIRPS.map(addweatherData);

// Create an ImageCollection from a multi-band image time series based on a band name
var flattenByBands = function(band) {
    var flattened = dataset.select(ee.String(band)).toBands();
    return flattened.set({"system:index": ee.String(band)});
};

// Generate band names
var bandNames = dataset.first().bandNames();
var flattenedByBands = ee.ImageCollection(bandNames.map(flattenByBands));

// Reduce regions and calculate statistics
var flattenedCollectionToTSstats = function(image) {
    var TSvalues = image.reduceRegions({
        reducer: 'mean',
        collection: rainGaugeSHP,
        scale: 5566,
        tileScale: 16
    });
    return TSvalues;
};

var finalResults = flattenedByBands.map(flattenedCollectionToTSstats);

// Export results
var inList = finalResults.toList(finalResults.size());
for (var i = 0; i < 2; i++) { // Export the first two datasets for testing
    var image = inList.get(i);

    Export.table.toDrive({
        collection: ee.FeatureCollection(image),
        description: ee.Image(image).get('system:index').getInfo(),
        fileNamePrefix: ee.Image(image).get('system:index').getInfo()
    });
}

