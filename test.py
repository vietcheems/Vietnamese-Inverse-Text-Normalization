import unittest
from inverse_normalize import inverse_normalize
class ITNTest(unittest.TestCase):
    def test_cardinal(self):
        cardinal = {
            "âm hai": "-2",
            "bốn lăm": "45",
            "trừ một tỷ chín triệu sáu trăm nghìn ba trăm hai mốt": "-1.009.600.321",
            "một trăm": "100",
            "chín trăm chín chín nghìn tỷ tỷ": "999.000.000.000.000.000.000.000",
            "hai nghìn không trăm linh năm": "2.005"
		}
        for case in cardinal.keys():
            self.assertEqual(inverse_normalize(case), cardinal[case])

    def test_date(self):
        date = {
            "năm năm mươi": "năm 50",
            "tháng chạp năm hai không hai mươi": "tháng 12/2020",
            "ngày mồng chín tháng tám": "ngày 09/08",
            "ngày rằm": "ngày 15",
            "tháng giêng": "tháng 1"
        }
        for case in date.keys():
            self.assertEqual(inverse_normalize(case), date[case])
    
    def test_consec_num(self):
        consec_num = {
            "một hai": "12",
            "hai năm": "25",
            "ba một bốn một": "3141",
            "ba hai năm": "325"
        }
        for case in consec_num.keys():
            self.assertEqual(inverse_normalize(case), consec_num[case])
    
    def test_decimal(self):
        decimal = {
            "không chấm hai mươi": "0.20",
            "một phẩy hai ba": "1,23",
            "năm phẩy năm triệu": "5.500.000",
            "năm nghìn bảy trăm bốn bốn phẩy bảy ba một": "5.744,731",
            "không phẩy một": "0,1",
            "một phẩy một ba năm nghìn": "1.135",
        }
        for case in decimal.keys():
            self.assertEqual(inverse_normalize(case), decimal[case])
    
    def test_fraction(self):
        fraction = {
            "một phần hai": "1/2",
            "âm hai phần bốn": "-2/4"
        }
        for case in fraction.keys():
            self.assertEqual(inverse_normalize(case), fraction[case])

    def test_measure(self):
        measure = {
            "hai mon": "2 mol",
            "năm xen ti mét trên giây": "5 cm/s",
            "hai năm": "2 năm"
        }
        for case in measure.keys():
            self.assertEqual(inverse_normalize(case), measure[case])

    def test_money(self):
        money = {
            "một phẩy hai triệu bảng anh": "1.200.000£",
            "một nghìn đồng": "1.000₫",
            "hai nghìn việt nam đồng": "2.000₫",
            "năm đô": "5$"
        }
        for case in money.keys():
            self.assertEqual(inverse_normalize(case), money[case])
    
    def test_time(self):
        time = {
            "một giờ": "1h",
            "mười hai giờ kém năm": "11h55",
            "hai rưỡi": "02h30",
            "hai giờ rưỡi": "02h30",
            "hai giờ ba mươi": "02h30",
            "hai giờ ba mươi phút": "02h30",
            "hai giờ hai phút hai giây": "02h02p02s",
            "ba mươi phút": "30p",
        }
        for case in time.keys():
            self.assertEqual(inverse_normalize(case), time[case])
if __name__ == "__main__":
	unittest.main()