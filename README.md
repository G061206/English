# English

## 四级高频词汇

本仓库包含大学英语四级（CET-4）高频词汇资料。

### 文件说明

- `四级高频词汇.pdf` - 原始PDF格式的四级高频词汇表
- `四级高频词汇.csv` - CSV格式的四级高频词汇表（773个词条）
- `convert_pdf_to_csv.py` - PDF转CSV的转换脚本

### CSV格式说明

CSV文件包含以下三列：
- `word` - 英语单词
- `part_of_speech` - 词性（如 n., v., a., vt., vi., ad. 等）
- `definition` - 中文释义

### 使用方法

CSV文件可以使用Excel、Google Sheets或任何支持CSV格式的工具打开，方便查阅和学习。

如需重新生成CSV文件，可运行：
```bash
python3 convert_pdf_to_csv.py
```