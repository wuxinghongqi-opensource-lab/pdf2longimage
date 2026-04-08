# pdf2longimage：PDF 转换长截图工具

# pdf2longimage: PDF to Long Image Tool

## 项目简介 / Introduction

`pdf2longimage` 是一款轻量级命令行工具，用于将多页 PDF 文件转换为单张长截图。

`pdf2longimage` is a lightweight command-line tool that converts multi-page PDF files into a single long screenshot image.

## 核心功能 / Features

- 多页 PDF 合并为一张纵向长图
    
- 支持自定义输出路径与临时目录
    
- 快速转换，带进度条显示
    
- 高清渲染，画质清晰
    
- Convert multi-page PDF into one long vertical image
    
- Support custom output path and temp directory
    
- Fast conversion with progress bar
    
- High-definition rendering
    

## 依赖安装 / Dependencies Installation


```
pip install Pillow
pip install tqdm
pip install PyMuPDF
```

## 基础用法 / Basic Usage

### 基础用法（默认输出路径）

### Default Usage (Default Output Path)


```
Pdf2Longimage --pdf_path C:\Users\Administrator\Desktop\Pdf2Longimage\1.PDF
```


## 参数说明 / Parameters

- `--pdf_path` **（必填）** 输入 PDF 文件路径
    
- `--pdf_path` **(Required)** Path of the input PDF file
