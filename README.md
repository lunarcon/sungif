# sungif

Download solar imagery from a certain datespan and create a gif.
Data source: suntoday.lmsal.com (SDO)

Usage: python sungif.py [start_date] [end_date] [resolution] [wavelength/combination/src]
- start_date: date in format YYYY-MM-DD (optional, defaults to 2024-01-01)
- end_date: date in format YYYY-MM-DD (optional, defaults to today)
- resolution: 'l' or 'f' (optional, defaults to 'l', l = 1K, f = 4K)
- wavelength/combination/src: (optional, defaults to '0304')
```
Avaibable wavelenghts/combinations:

   -  0304
   -  1600
   -  1700
   -  _304_211_171
   -  _094_335_193
   -  094
   -  335
   -  131
   -  _211_193_171
   -  211
   -  193
   -  171
   -  _HMI_cont_aiascale
   -  _HMImag
   -  _HMImag_171
```

If you set the two dates to be the same, a single image is downloaded and saved as a jpg.

## Upcoming
- Ability to save as image sequence
- Ability to save as video (mp4, etc)
- fix option handling
- ability to specify custom resolution, image of closest resolution is downloaded and is rescaled.
