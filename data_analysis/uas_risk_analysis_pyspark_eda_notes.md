# UAS Risk Analysis EDA Notes:

* Full OpenSky network track points dataset spans `2023-01-01 00:00:01` through `2024-10-05 23:59:59`, which represents `643 days (1.76 years)`, with a total of `1,363,536,638` track point records.
* Track points are recorded at 1hz or 1 track point per second.
* UAS Sightings dataset spans `2023-06-01 00:00:00` through `2024-09-30 00:00:00`, which represents 487 days (1.33 years), with a total of `2,274` sightings records.
* Applying filter to capture overlap between track points and uas sightings records reduced the dataset from `1,363,536,638` track points to `1,342,986,693` records (reduced by `20,549,945` records).
* After syncing track points with UAS sightings data, sampling the track points to reduce density, and loading only the last two months (`2024-08-01` through `2024-09-30`), we have sufficiently reduced the dataset such that the memory footprint is small enough to persist in memory and disk with a total of `7,321,049` track point records.

## Descriptive Statistics
**After sync with UAS sightings**

```
-RECORD 0------------------------------
 summary        | count                
 icao24         | 49998420             
 lat            | 49727087             
 lon            | 49727087             
 velocity       | 47802859             
 heading        | 47802859             
 vertrate       | 47804212             
 callsign       | 49360749             
 onground       | 49998420             
 alert          | 49998420             
 spi            | 49998420             
 squawk         | 22898397             
 baroaltitude   | 45773661             
 geoaltitude    | 45556492             
 lastposupdate  | 49727087             
 lastcontact    | 49998420             
 day_of_week    | 49998420             
 daynum_of_week | 49998420             
-RECORD 1------------------------------
 summary        | mean                 
 icao24         | Infinity             
 lat            | 37.232219770952405   
 lon            | -94.92576574645094   
 velocity       | 147.27921312644133   
 heading        | 180.20366616677566   
 vertrate       | -0.5327892205916664  
 callsign       | 1498659.2643357618   
 onground       | 0.08143001318841675  
 alert          | 0.018145613401383483 
 spi            | 0.012463093833765147 
 squawk         | 3701.551175612861    
 baroaltitude   | 5420.874708393164    
 geoaltitude    | 5566.867753559688    
 lastposupdate  | 1.7109235012170017E9 
 lastcontact    | 1.71092679966351E9   
 day_of_week    | null                 
 daynum_of_week | 4.002313253098798    
-RECORD 2------------------------------
 summary        | stddev               
 icao24         | NaN                  
 lat            | 5.337792671186345    
 lon            | 16.697018801093098   
 velocity       | 82.43210850002413    
 heading        | 101.739372106976     
 vertrate       | 4.841764566620834    
 callsign       | 8149270.28612333     
 onground       | 0.27349436490827683  
 alert          | 0.1334779025607209   
 spi            | 0.11094036854102762  
 squawk         | 2221.0820681416913   
 baroaltitude   | 4422.323560232944    
 geoaltitude    | 4527.307496445753    
 lastposupdate  | 9003546.098797055    
 lastcontact    | 9003590.5827863      
 day_of_week    | null                 
 daynum_of_week | 2.0065677215281177   
-RECORD 3------------------------------
 summary        | min                  
 icao24         | 000280               
 lat            | -41.39108431541314   
 lon            | -179.94693837267286  
 velocity       | 0.0                  
 heading        | 0.0                  
 vertrate       | -165.8112            
 callsign       |                      
 onground       | 0                    
 alert          | 0                    
 spi            | 0                    
 squawk         | 0000                 
 baroaltitude   | -982.98              
 geoaltitude    | -998.22              
 lastposupdate  | 1.696118397817E9     
 lastcontact    | 1.69611840093E9      
 day_of_week    | Friday               
 daynum_of_week | 1                    
-RECORD 4------------------------------
 summary        | max                  
 icao24         | fb1f38               
 lat            | 66.44247436523438    
 lon            | 176.82122802734375   
 velocity       | 2974.157691531427    
 heading        | 359.89310501299224   
 vertrate       | 165.8112             
 callsign       | ZUF 250              
 onground       | 1                    
 alert          | 1                    
 spi            | 1                    
 squawk         | 7777                 
 baroaltitude   | 38648.64             
 geoaltitude    | 39090.6              
 lastposupdate  | 1.72765439898E9      
 lastcontact    | 1.72765439898E9      
 day_of_week    | Wednesday            
 daynum_of_week | 7
```

**After sampling and targeting last two months:**

```
-RECORD 0------------------------------
 summary        | count                
 icao24         | 7321049              
 lat            | 7281222              
 lon            | 7281222              
 velocity       | 7001085              
 heading        | 7001085              
 vertrate       | 7001316              
 callsign       | 7229348              
 onground       | 7321049              
 alert          | 7321049              
 spi            | 7321049              
 squawk         | 2316338              
 baroaltitude   | 6683153              
 geoaltitude    | 6662395              
 lastposupdate  | 7281222              
 lastcontact    | 7321049              
 day_of_week    | 7321049              
 daynum_of_week | 7321049              
 month_name     | 7321049              
-RECORD 1------------------------------
 summary        | mean                 
 icao24         | Infinity             
 lat            | 37.70793471656258    
 lon            | -95.16787965495026   
 velocity       | 143.81032238429202   
 heading        | 179.5665046881646    
 vertrate       | -0.5680158432385914  
 callsign       | 4940750.819394561    
 onground       | 0.08262354206343928  
 alert          | 0.015044428742383776 
 spi            | 0.011040357741083279 
 squawk         | 3696.223444074224    
 baroaltitude   | 5191.284273794066    
 geoaltitude    | 5456.271401623613    
 lastposupdate  | 1.7250524570916262E9 
 lastcontact    | 1.7250523255637517E9 
 day_of_week    | null                 
 daynum_of_week | 4.042356088587852    
 month_name     | null                 
-RECORD 2------------------------------
 summary        | stddev               
 icao24         | NaN                  
 lat            | 5.443313396633557    
 lon            | 16.944844735491177   
 velocity       | 82.39057887561451    
 heading        | 101.88934422668063   
 vertrate       | 4.779981693545755    
 callsign       | 1.5163685036423005E7 
 onground       | 0.27531237297588795  
 alert          | 0.12172960170081522  
 spi            | 0.1044914816308615   
 squawk         | 2193.513157503549    
 baroaltitude   | 4385.48337065914     
 geoaltitude    | 4613.553183786       
 lastposupdate  | 1499667.663860112    
 lastcontact    | 1499720.8913076464   
 day_of_week    | null                 
 daynum_of_week | 2.035309465944983    
 month_name     | null                 
-RECORD 3------------------------------
 summary        | min                  
 icao24         | 002034               
 lat            | -22.763809204101562  
 lon            | -175.14505004882812  
 velocity       | 0.0                  
 heading        | 0.0                  
 vertrate       | -165.8112            
 callsign       |                      
 onground       | 0                    
 alert          | 0                    
 spi            | 0                    
 squawk         | 0000                 
 baroaltitude   | -472.44000000000005  
 geoaltitude    | -685.8               
 lastposupdate  | 1.722470293304E9     
 lastcontact    | 1.722470400854E9     
 day_of_week    | Friday               
 daynum_of_week | 1                    
 month_name     | August               
-RECORD 4------------------------------
 summary        | max                  
 icao24         | e80241               
 lat            | 64.90040588378906    
 lon            | 120.2191267342403    
 velocity       | 1940.61478413284     
 heading        | 359.8920984712272    
 vertrate       | 165.8112             
 callsign       | ZEUS34               
 onground       | 1                    
 alert          | 1                    
 spi            | 1                    
 squawk         | 7777                 
 baroaltitude   | 38618.16             
 geoaltitude    | 38823.9              
 lastposupdate  | 1.72765439898E9      
 lastcontact    | 1.72765439898E9      
 day_of_week    | Wednesday            
 daynum_of_week | 7                    
 month_name     | September
```
