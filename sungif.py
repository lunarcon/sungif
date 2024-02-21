import requests, datetime, io, PIL.Image, imageio, sys

URL_FORMAT = ['https://suntoday.lmsal.com/sdomedia/SunInTime/{}/{}{}.jpg', "%Y/%m/%d"]
WAVS = [
    "0304", "1600", "1700", "_304_211_171",
    "_094_335_193", "094", "335", "131",
    "_211_193_171", "211", "193", "171",
    "_HMI_cont_aiascale", "_HMImag", "_HMImag_171"
]

def get_image(date, res, wav):
    dat = date.strftime(URL_FORMAT[1])
    url = URL_FORMAT[0].format(dat, res, wav)
    print("getting image for", date, url, end='... ')
    response = requests.get(url)
    if response.status_code == 200:
        print("✅")
        return response.content
    else:
        print("❌")
        return None
    
def create_image(image_data):
    image = PIL.Image.open(io.BytesIO(image_data))
    return image

def datespan(startDate, endDate, delta=datetime.timedelta(days=1)):
    currentDate = startDate
    while currentDate <= endDate:
        yield currentDate
        currentDate += delta

def closest(wav):
    return max(WAVS, key=lambda x: len(set(wav) & set(x)))

def main():
    date = datetime.date(2024, 1, 1)
    end_date = datetime.date.today()
    images = []
    res = 'l'
    wav = '0304'
    if len(sys.argv)  == 1:
        sys.argv.append('help')
    if len(sys.argv) > 1:
        if sys.argv[1] == 'help':
            print("Usage: python sungif.py [start_date] [end_date] [resolution] [wavelength/combination/src]")
            print("  start_date: date in format YYYY-MM-DD (optional, defaults to 2024-01-01)")
            print("  end_date: date in format YYYY-MM-DD (optional, defaults to today)")
            print("  resolution: 'l' or 'f' (optional, defaults to 'l', l = 1K, f = 4K)")
            print("  wavelength/combination/src: (optional, defaults to '0304')\n\t-\t"+'\n\t-\t'.join(WAVS))
            return
        try:
            date = datetime.datetime.strptime(sys.argv[1], '%Y-%m-%d').date()
        except ValueError:
            print("Invalid date, must be in format YYYY-MM-DD")
            return
    if len(sys.argv) > 2:
        try:
            end_date = datetime.datetime.strptime(sys.argv[2], '%Y-%m-%d').date()
        except ValueError:
            print("Invalid date, must be in format YYYY-MM-DD")
            return
    if len(sys.argv) > 3:
        res = sys.argv[3]
        if res not in ['l', 'f']:
            print("Invalid resolution, must be 'l' or 'f'")
            return
    if len(sys.argv) > 4:
        wav = sys.argv[4]
        if wav not in WAVS:
            print("Invalid wavelength/combination/src, did you mean: "+ closest(wav) + "?")
            return
    
    for dt in datespan(date, end_date):
        image_data = get_image(dt, res, wav)
        if image_data:
            image = create_image(image_data)
            images.append(image)
    
    if len(images) == 0:
        print('❌')
        return
    if len(images) == 1:
        images[0].save('sungif_{}_{}_{}_{}.jpg'.format(res, date, end_date, wav))
        print('creating sungif_{}_{}_{}_{}.jpg ...'.format(res, date, end_date, wav), end=' ')
    else:
        print('creating sungif_{}_{}_{}_{}.gif ...'.format(res, date, end_date, wav), end=' ')
        imageio.mimsave('sungif_{}_{}_{}_{}.gif'.format(res, date, end_date, wav), images)
    print('✅')

if __name__ == '__main__':
    main()
