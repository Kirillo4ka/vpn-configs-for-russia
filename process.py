#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EaveVPN Processor - Fetches, processes and pushes VPN configs
"""

import requests
import re
import os
import json
import subprocess
from urllib.parse import unquote
from datetime import datetime

# === НАСТРОЙКИ ===
SOURCE_REPO = os.getenv("SOURCE_REPO", "igareck/vpn-configs-for-russia")
SOURCE_BRANCH = os.getenv("SOURCE_BRANCH", "main")
DEST_REPO = os.getenv("DEST_REPO", "Kirillo4ka/eavevpn-configs")
DEST_BRANCH = os.getenv("DEST_BRANCH", "main")
BRAND_NAME = os.getenv("BRAND_NAME", "EaveVPN")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
FILE_EXTENSIONS = os.getenv("FILE_EXTENSIONS", "txt").split(",")

# Страны
COUNTRIES = {
    '🇷🇺': ('RU', 'Россия'), '🇺🇦': ('UA', 'Украина'), '🇩': ('DE', 'Германия'),
    '🇳🇱': ('NL', 'Нидерланды'), '🇫🇷': ('FR', 'Франция'), '🇬': ('GB', 'Великобритания'),
    '🇪🇸': ('ES', 'Испания'), '🇮🇹': ('IT', 'Италия'), '🇵🇱': ('PL', 'Польша'),
    '🇷🇴': ('RO', 'Румыния'), '🇧🇪': ('BE', 'Бельгия'), '🇬🇷': ('GR', 'Греция'),
    '🇵🇹': ('PT', 'Португалия'), '🇨🇿': ('CZ', 'Чехия'), '🇭': ('HU', 'Венгрия'),
    '🇸🇪': ('SE', 'Швеция'), '🇦': ('AT', 'Австрия'), '🇨🇭': ('CH', 'Швейцария'),
    '🇨🇳': ('CN', 'Китай'), '🇯🇵': ('JP', 'Япония'), '🇰🇷': ('KR', 'Южная Корея'),
    '🇮🇳': ('IN', 'Индия'), '🇸🇬': ('SG', 'Сингапур'), '🇹🇭': ('TH', 'Таиланд'),
    '🇻🇳': ('VN', 'Вьетнам'), '🇲🇾': ('MY', 'Малайзия'), '🇮': ('ID', 'Индонезия'),
    '🇺🇸': ('US', 'США'), '🇨': ('CA', 'Канада'), '🇧🇷': ('BR', 'Бразилия'),
    '🇦🇺': ('AU', 'Австралия'), '🇹🇷': ('TR', 'Турция'), '🇮🇷': ('IR', 'Иран'),
    '🇰': ('KZ', 'Казахстан'), '🇺🇿': ('UZ', 'Узбекистан'), '🇬🇪': ('GE', 'Грузия'),
}

TEXT_TO_FLAG = {
    'russia': '🇷🇺', 'россия': '🇷🇺', 'ukraine': '🇺', 'украина': '🇦',
    'germany': '🇩🇪', 'германия': '🇩🇪', 'de': '🇩', 'netherlands': '🇱',
    'нидерланды': '🇳🇱', 'nl': '🇳🇱', 'france': '🇫🇷', 'франция': '🇫🇷',
    'uk': '🇬', 'великобритания': '🇬🇧', 'usa': '🇺🇸', 'сша': '🇺🇸',
    'canada': '🇨🇦', 'japan': '🇯', 'япония': '🇯🇵', 'korea': '🇰🇷', 'корея': '🇰🇷',
    'india': '🇮🇳', 'индия': '🇮', 'china': '🇳', 'китай': '🇨',
    'poland': '🇵', 'польша': '🇵🇱', 'turkey': '🇹🇷', 'турция': '🇹🇷',
    'kazakhstan': '🇰', 'казахстан': '🇰🇿',
}

WHITE_KEYWORDS = ['white', 'allow', 'safe', 'белый', 'разреш']
BLACK_KEYWORDS = ['black', 'block', 'ban', 'черный', 'запрет']
PROTOCOLS = ['vless', 'vmess', 'trojan', 'ss', 'ssr', 'hysteria', 'tuic', 'socks', 'http', 'https', 'wireguard']


def detect_list_type(filename):
    name = filename.lower()
    w = sum(1 for kw in WHITE_KEYWORDS if kw in name)
    b = sum(1 for kw in BLACK_KEYWORDS if kw in name)
    return 'White List' if w > b else 'Black List'


def detect_country(name):
    if not name:
        return '', 'Proxy'
    decoded = unquote(name).lower()
    for flag, (code, ru) in COUNTRIES.items():
        if flag in name:
            return flag, ru
    for key, flag in TEXT_TO_FLAG.items():
        if key in decoded and flag in COUNTRIES:
            return flag, COUNTRIES[flag][1]
    return '', 'Proxy'


def detect_ip_type(host):
    if not host:
        return 'Unknown'
    if ':' in host and ('::' in host or host.count(':') >= 2):
        return 'IPv6'
    if re.match(r'^\d{1,3}(\.\d{1,3}){3}$', host):
        return 'IPv4'
    return 'Domain'


def get_protocol(link):
    link_lower = link.lower().strip()
    for proto in PROTOCOLS:
        if link_lower.startswith(proto + '://'):
            return proto.upper()
    return None


def parse_link(link, counter, list_type):
    try:
        link = link.strip()
        if not link or link.startswith('#'):
            return None
        
        proto = get_protocol(link)
        if not proto:
            return link
        
        host = ''
        if '@' in link:
            parts = link.split('@')
            if len(parts) > 1:
                host = parts[1].split('/')[0].split('?')[0].split(':')[0].replace('[', '').replace(']', '')
        
        if '#' in link:
            base = link.rsplit('#', 1)[0]
            old_name = link.rsplit('#', 1)[1]
        else:
            base = link
            old_name = ''
        
        flag, country = detect_country(old_name)
        if not flag:
            ip_type = detect_ip_type(host)
            if ip_type in ('IPv4', 'IPv6'):
                flag, country = '', f'Proxy {ip_type}'
            else:
                flag, country = '', 'Proxy'
        
        name = f"{flag} {country} | {list_type} | Fast | {BRAND_NAME} | #{counter:04d}"
        return f"{base}#{name}"
    except:
        return None


def generate_header(count, filename):
    now = datetime.now().strftime("%Y-%m-%d / %H:%M")
    name_clean = filename.rsplit('.', 1)[0].replace('-', ' ').replace('_', ' ').title()
    return f"""# profile-title: {name_clean} | EaveVPN
# profile-update-interval: 5
# Date/Time: {now} (Moscow)
# Count: {count}
# Source: github.com/{SOURCE_REPO}
# Info: github.com/Kirillo4ka/eavevpn-configs

"""


def fetch_source_files():
    url = f"https://api.github.com/repos/{SOURCE_REPO}/contents?ref={SOURCE_BRANCH}"
    headers = {'Accept': 'application/vnd.github.v3+json'}
    
    try:
        resp = requests.get(url, headers=headers, timeout=30)
        if resp.status_code != 200:
            print(f"❌ API error: {resp.status_code}")
            return []
        
        items = resp.json()
        if not isinstance(items, list):
            return []
        
        files = []
        for item in items:
            if item.get('type') == 'file':
                name = item.get('name', '')
                ext = name.split('.')[-1].lower() if '.' in name else ''
                if ext in FILE_EXTENSIONS:
                    files.append({
                        'name': name,
                        'list_type': detect_list_type(name),
                        'raw_url': item.get('download_url'),
                        'size': item.get('size', 0)
                    })
        return files
    except Exception as e:
        print(f"❌ Fetch error: {e}")
        return []


def download_file(url):
    try:
        resp = requests.get(url, timeout=30)
        resp.raise_for_status()
        return resp.text
    except:
        return None


def process_file_content(content, list_type):
    lines = content.splitlines()
    result = []
    counter = 1
    
    for line in lines:
        line = line.strip()
        if line.startswith('# profile-') or line.startswith('# Date/') or line.startswith('# Count:'):
            continue
        if not line:
            continue
        
        processed = parse_link(line, counter, list_type)
        if processed:
            result.append(processed)
            counter += 1
    
    return result, counter - 1


def main():
    print("🚀 EaveVPN Processor started")
    print(f"📥 Source: {SOURCE_REPO}@{SOURCE_BRANCH}")
    print(f"📤 Dest: {DEST_REPO}@{DEST_BRANCH}")
    
    files = fetch_source_files()
    if not files:
        print("⚠️ No files found")
        return
    
    print(f"📁 Found {len(files)} files")
    
    total_links = 0
    processed_files = []
    
    for f in files:
        print(f"\n📄 Processing: {f['name']} [{f['list_type']}]")
        
        content = download_file(f['raw_url'])
        if not content:
            print(f"   ⚠️ Skipped")
            continue
        
        links, count = process_file_content(content, f['list_type'])
        if count == 0:
            print(f"   ⚠️ No links")
            continue
        
        header = generate_header(count, f['name'])
        output = header + '\n'.join(links)
        
        with open(f['name'], 'w', encoding='utf-8') as out:
            out.write(output)
        
        processed_files.append(f['name'])
        total_links += count
        print(f"   ✅ {count} links → {f['name']}")
    
    if not processed_files:
        print("\n⚠️ No files processed")
        return
    
    print(f"\n✅ Done: {len(processed_files)} files, {total_links} links")
    
    with open('.processed_files.json', 'w') as f:
        json.dump({'files': processed_files, 'total_links': total_links}, f)


if __name__ == '__main__':
    main()