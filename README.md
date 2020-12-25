# CS321 Ngôn ngữ học ngữ liệu
* GVHD: Nguyễn Thị Quý
* Nhóm thực hiện:
1. Dương Lê Tường Khang 18520882
2. Bùi Đào Gia Huy 18520818
3. Lã Trường Hải 18520698
### Bộ mã này được viết lại từ bộ RDRSegmenter: https://github.com/datquocnguyen/RDRsegmenter
	@InProceedings{NguyenNVDJ2018,
	author={Dat Quoc Nguyen and Dai Quoc Nguyen and Thanh Vu and Mark Dras and Mark Johnson},
	title={{A Fast and Accurate Vietnamese Word Segmenter}},
	booktitle={Proceedings of the 11th International Conference on Language Resources and Evaluation (LREC 2018)},
	pages={2582--2587},
	year={2018}
	}
**Please CITE** our paper whenever RDRsegmenter is used to produce published results or incorporated into other software. 
Các bước thực hiện

### Bước 1: Train với tập dữ liệu mới
Bỏ dữ liệu vào folder train
// python DataPreprocessor.py file_train.txt
