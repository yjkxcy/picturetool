import shutil
from PIL import Image
from PIL import ImageFile
from pathlib import Path



def auto_summary(srcpath, destpath, ftype='*.jpg'):
	'''扫描目录下指定文件，汇总到指定文件中'''
	for fname in Path(srcpath).rglob(ftype):
		destfile = Path(destpath, Path(fname).name)
		# print(destfile)
		if destfile.exists():
			print(f'文件存在: {fname}  {destfile}')
			continue
		try:
			shutil.copy2(fname, destfile)
		except Exception as e:
			print(f'复制出错: {fname}')

def compress_image(outfile, kb=95, quality=85, k=0.9):
	'''把图片压缩到指定大小，文件大小单位:kb'''
	o_size = Path(outfile).stat().st_size // 1024
	print(o_size)
	print('before_size: {} after_size: {}'.format(o_size, kb))
	if o_size <= kb:
		return outfile
	ImageFile.LOAD_TRUNCATED_IMAGES = True
	while o_size > kb:
		im = Image.open(outfile)
		x, y = im.size
		out = im.resize((int(x*k), int(y*k)), Image.Resampling.LANCZOS)
		try:
			out.save(outfile, quality=quality)
		except Exception as e:
			print(e)
			break
		o_size = Path(outfile).stat().st_size // 1024
	return outfile

def batch_compression(fpath, fsizeKb=98, ftype='*.jpg'):
	'''批量压缩文件至指定大小(单位kb)，默认: jpg'''
	for fname in Path(fpath).rglob(ftype):
		compress_image(fname, kb=fsizeKb)

def pngtojpg(fname):
	'''png转jpg'''
	fpath = Path(fname).parent
	newfname = f'{Path(fname).stem}.jpg'
	print(f'new: {newfname}, old: {fname}')
	im = Image.open(fname).convert("RGB")
	im.save(Path(fpath, newfname), quality=95)
	return newfname

def batch_ftype_convert(fpath, converter=pngtojpg, srctype='*.png'):
	'''批量文件类型转换, 默认：png转jpg'''
	for fname in Path(fpath).rglob(srctype):
		converter(fname)



if __name__ == '__main__':
	srcpath = r'C:\Users\user\Desktop\tttt'
	despath = r'C:\Users\user\Desktop\pic'
	print(len(list(Path(srcpath).rglob('*.jpg'))))          #统计jpg文件数量
	print(len(list(Path(srcpath).rglob('*.png'))))          #统计png文件数量
	auto_summary(srcpath, despath, ftype='*.jpg')           #汇总到指定目录
	# batch_ftype_convert(srcpath)                            #png转jpg
	batch_compression(srcpath)                              #压缩到95Kb
	print('end')

