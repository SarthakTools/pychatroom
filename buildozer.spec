[app]

title = MayBee
package.name = maybee
package.domain = org.maybee

source.dir = .
source.include_exts = py,png,jpg,kv,atlas

version = 1.0

requirements = python3==3.11.6,hostpython3==3.11.6,kivy==2.2.1,kivymd==1.1.1,cython==0.29.33,requests,urllib3,certifi,chardet,idna,charset_normalizer

orientation = portrait
fullscreen = 0

# Android specific
android.permissions = INTERNET
android.api = 33
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license = True
android.archs = arm64-v8a

# Pin p4a to the stable master branch (not develop, which requires
# Python 3.14 and is still unstable as of mid-2026)
p4a.branch = master

[buildozer]
log_level = 2
warn_on_root = 1
