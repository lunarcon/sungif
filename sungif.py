import requests, datetime, io, PIL.Image, imageio, sys

URL_FORMATS = {'sdo_blank': 'https://www.spaceweather.com/images%Y/%d%b%y/coronalhole_sdo_blank.jpg',
               'hmi': 'https://www.spaceweather.com/images%Y/%d%b%y/hmi4096_blank.jpg',
               'sdo_304nm': 'https://suntoday.lmsal.com/sdomedia/SunInTime/%Y/%m/%d/l0304.jpg',
               }

def get_image(date, src):
    url = date.strftime(src).lower()
    print("getting image for", date, url, end='... ')
    response = requests.get(url)
    if response.status_code == 200:
        print("✅")
        return response.content
    else:
        print("❌")
        return None
    
def create_image(date, image_data):
    image = PIL.Image.open(io.BytesIO(image_data))
    return image

def datespan(startDate, endDate, delta=datetime.timedelta(days=1)):
    currentDate = startDate
    while currentDate < endDate:
        yield currentDate
        currentDate += delta

def main():
    date = datetime.date(2024, 1, 1)
    end_date = datetime.date.today()
    images = []
    frmt = 'hmi'

    if len(sys.argv) > 1:
        if sys.argv[1] == 'help':
            print("Usage: python sungif.py [format] [start_date] [end_date]")
            print("  format: ", ' | '.join(list(URL_FORMATS.keys())))
            print("  start_date: date in format YYYY-MM-DD (optional, defaults to 2024-01-01)")
            print("  end_date: date in format YYYY-MM-DD (optional, defaults to today)")
            return
        frmt = sys.argv[1]
    if len(sys.argv) > 2:
        date = datetime.datetime.strptime(sys.argv[2], '%Y-%m-%d').date()
    if len(sys.argv) > 3:
        end_date = datetime.datetime.strptime(sys.argv[3], '%Y-%m-%d').date()
    if frmt not in URL_FORMATS:
        print(f"Invalid format {frmt}, must be one of:\n{', '.join(list(URL_FORMATS.keys()))}")
        return
    
    for dt in datespan(date, end_date):
        image_data = get_image(dt, URL_FORMATS[frmt])
        if image_data:
            image = create_image(dt, image_data)
            images.append(image)
    
    print(f"Saving {len(images)} images to {frmt}.gif")
    imageio.mimsave('sungif_{}_{}_{}.gif'.format(frmt, date, end_date), images)

if __name__ == '__main__':
    main()
