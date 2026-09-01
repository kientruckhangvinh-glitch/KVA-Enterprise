# 11_Automation - Hệ Thống Tự Động Hóa Doanh Nghiệp

[![CI/CD Pipeline](https://github.com/KVA-Enterprise/11_Automation/actions/workflows/sales-pipeline-sync.yml/badge.svg)](https://github.com/KVA-Enterprise/11_Automation/actions)
[![Python Version](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-Proprietary-green.svg)](LICENSE)

**Hệ thống CI/CD, Cronjobs và Workflows tự động hóa cho KVA Enterprise**

---

## 📋 Mục Lục

- [Tổng Quan](#-tổng-quan)
- [Kiến Trúc Hệ Thống](#-kiến-trúc-hệ-thống)
- [Cấu Trúc Repository](#-cấu-trúc-repository)
- [Workflows](#-workflows)
- [Scripts](#-scripts)
- [Cài Đặt](#-cài-đặt)
- [Cấu Hình](#-cấu-hình)
- [Sử Dụng](#-sử-dụng)
- [Tài Liệu Liên Quan](#-tài-liệu-liên-quan)

---

## 📊 Tổng Quan

Repository này chứa toàn bộ hệ thống tự động hóa của KVA Enterprise, bao gồm:

✅ **GitHub Actions Workflows** - CI/CD pipelines tự động  
✅ **Python Scripts** - Xử lý dữ liệu, tích hợp AI (Claude), tạo báo cáo  
✅ **Automation Rules** - Áp dụng SOP-SAL-001 và các quy trình nghiệp vụ  
✅ **Integration** - Kết nối Google Sheets, Anthropic Claude, Email/Slack  

### Tính Năng Chính

| Tính Năng | Mô Tả | Frequency |
|-----------|-------|-----------|
| **Sales Pipeline Sync** | Đồng bộ dữ liệu từ Google Sheets → 10_Data | Hàng ngày 17:00 |
| **CEO AI Report** | Tạo báo cáo tuần bằng Claude AI | Thứ 2 hàng tuần 08:00 |
| **Alert System** | Cảnh báo RULE-SAL-001 đến 007 | Real-time |
| **Contract Generator** | Tự động tạo hợp đồng khi deal WON | On-demand |

---

## 🏗️ Kiến Trúc Hệ Thống
