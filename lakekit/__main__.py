"""检查指定原始资料，不生成仓库发布版本。"""
import argparse
import json
from .inventory import load

def main():
    parser=argparse.ArgumentParser(description='实验原始资料清单检查')
    parser.add_argument('manifest')
    args=parser.parse_args()
    print(json.dumps(load(args.manifest),ensure_ascii=False,indent=2))

if __name__=='__main__':
    main()
