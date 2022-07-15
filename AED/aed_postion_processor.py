import urllib.request
import csv
import os
import math


class DataProcessor():

    def __init__(self, dir="data", filename="aed.csv", url="http://es.hkfsd.gov.hk/aed_api/export_aed.php?lang=EN") -> None:
        self.dir = dir
        self.filename = filename
        self.url = url
        self.positions = []
        self.information = []

        self.download()

    def download(self):
        if not os.path.exists(self.dir):
            os.mkdir(self.dir)
        path = os.path.join(self.dir, "aed.csv")
        if not os.path.exists(path):
            urllib.request.urlretrieve(url=self.url, filename=path)
            print("Download finished")

        self.parse(path)

    def schechule_download(self):
        try:
            path = os.path.join(self.dir, "aed.csv")
            urllib.request.urlretrieve(url=self.url, filename=path)

        except:
            pass

    def parse(self, path):
        path = path.replace("\\", "/")
        csv_reader = csv.reader(open(path, encoding='UTF-8'))
        read_name = True

        for line in csv_reader:
            if read_name:
                read_name = False
            else:
                lat = float(line[3])
                lng = float(line[4])
                if lat == 0 or lng == 0:
                    continue
                self.positions.append((lng, lat))

                name = line[0]
                address = line[1]
                detail = line[2]
                self.information.append((name, address, detail))

    def closest_k(self, lng, lat, k):

        closest_tuples = []

        for idx in range(len(self.positions)):
            p_lng, p_lat = self.positions[idx]
            p_name, p_addr, p_detail = self.information[idx]
            distance = self.cal_distance(lng, lat, p_lng, p_lat)

            if len(closest_tuples) < k:
                closest_tuples.append((distance, p_lng, p_lat, p_name, p_addr, p_detail))
                closest_tuples.sort()

            elif distance < closest_tuples[-1][0]:
                closest_tuples.pop()
                closest_tuples.append((distance, p_lng, p_lat, p_name, p_addr, p_detail))
                closest_tuples.sort()

        return closest_tuples

    def cal_distance(self, lng1, lat1, lng2, lat2):
        dx = lng1 - lng2
        dy = lat1 - lat2
        avg_lat = (lat1 + lat2) / 2.0
        lx = math.radians(dx) * math.cos(math.radians(avg_lat)) * 6367000.0
        ly = math.radians(dy) * 6367000.0
        return round(math.sqrt(lx * lx + ly * ly), 3)


if __name__ == "__main__":

    processor = DataProcessor("data", "aed.csv", "http://es.hkfsd.gov.hk/aed_api/export_aed.php?lang=EN")
    processor.closest_k(114.142744, 22.2801, 20)

