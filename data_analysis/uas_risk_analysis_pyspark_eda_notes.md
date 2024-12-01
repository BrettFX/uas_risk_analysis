# UAS Risk Analysis EDA Notes:

* Full OpenSky network track points dataset spans `2023-01-01 00:00:01` through `2024-10-05 23:59:59`, which represents `643 days (1.76 years)`, with a total of `1,363,536,638` track point records.
* Track points are recorded at 1hz or 1 track point per second.
* UAS Sightings dataset spans `2023-06-01 00:00:00` through `2024-09-30 00:00:00`, which represents 487 days (1.33 years), with a total of `2,274` sightings records.
* Applying filter to capture overlap between track points and uas sightings records reduced the dataset from `1,363,536,638` track points to `1,342,986,693` records (reduced by `20,549,945` records).
* After syncing track points with UAS sightings data, sampling the track points to reduce density, and loading only the last two months (`2024-08-01` through `2024-09-30`), we have sufficiently reduced the dataset such that the memory footprint is small enough to persist in memory and disk with a total of `7,321,049` track point records.