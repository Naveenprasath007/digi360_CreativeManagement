
# CM-360

CM-360 is Creative Management tool for Manage creatives.




## Authors

- [@Pranav Vijay](https://git.benefitalign.com/pranav.vijay)
- [@Naveen Kumaran](https://git.benefitalign.com/naveen.kumaran)


## Documentation

[Demo Input](https://git.benefitalign.com/truecoverage/creator-management)

[Demo output](https://git.benefitalign.com/truecoverage/creator-management)


## Installation

pip install -r requirments.txt

```bash
  git clone https://git.benefitalign.com/truecoverage/creator-management.git
  cd  DigitalMarketing
```
    

## Folder struture 
```bash
¦   .env
¦   .gitignore
¦   docker-compose.yml
¦   Dockerfile
¦   docker_cmd.txt
¦   entrypoint.sh
¦   README.md
¦   requirements.txt
¦   
+---DigitalMarketing
¦   ¦   .env
¦   ¦   alter table.txt
¦   ¦   LIST OUT THE DB.txt
¦   ¦   manage.py
¦   ¦   models.py
¦   ¦   postgre sql cmd.sql
¦   ¦   
¦   +---DigitalMarketing
¦   ¦       admin.py
¦   ¦       apps.py
¦   ¦       forms.py
¦   ¦       models.py
¦   ¦       tests.py
¦   ¦       urls.py
¦   ¦       validators.py
¦   ¦       views.py
¦   ¦       __init__.py
¦   ¦       
¦   +---media
¦   +---static
¦   ¦   +---css
¦   ¦   ¦       dash_style.css
¦   ¦   ¦       dash_style.css.map
¦   ¦   ¦       dash_style.scss
¦   ¦   ¦       dash_variables.css
¦   ¦   ¦       dash_variables.css.map
¦   ¦   ¦       dash_variables.scss
¦   ¦   ¦       style.css
¦   ¦   ¦       style.css.map
¦   ¦   ¦       style.scss
¦   ¦   ¦       styleold.css
¦   ¦   ¦       _variables.scss
¦   ¦   ¦       
¦   ¦   +---images
¦   ¦   ¦       accessgiven.png
¦   ¦   ¦       accessgivened.png
¦   ¦   ¦       animation.svg
¦   ¦   ¦       avatar.png
¦   ¦   ¦       av_1.png
¦   ¦   ¦       av_5.png
¦   ¦   ¦       cdn.png
¦   ¦   ¦       download.png
¦   ¦   ¦       Download.svg
¦   ¦   ¦       drive.svg
¦   ¦   ¦       enterview.svg
¦   ¦   ¦       facebook.svg
¦   ¦   ¦       facebook_1.svg
¦   ¦   ¦       fileupload.svg
¦   ¦   ¦       folder.svg
¦   ¦   ¦       GDN.svg
¦   ¦   ¦       Gif.svg
¦   ¦   ¦       grid-thumbnail.png
¦   ¦   ¦       grid.svg
¦   ¦   ¦       Hourglass.gif
¦   ¦   ¦       img.svg
¦   ¦   ¦       layout.png
¦   ¦   ¦       list.svg
¦   ¦   ¦       load.gif
¦   ¦   ¦       loading.gif
¦   ¦   ¦       logo_icon.png
¦   ¦   ¦       menu.png
¦   ¦   ¦       name.png
¦   ¦   ¦       name1.png
¦   ¦   ¦       native.svg
¦   ¦   ¦       picture.svg
¦   ¦   ¦       player.png
¦   ¦   ¦       playicon.png
¦   ¦   ¦       Select-all.svg
¦   ¦   ¦       settings.svg
¦   ¦   ¦       shape.svg
¦   ¦   ¦       shape_2.svg
¦   ¦   ¦       status.png
¦   ¦   ¦       success.png
¦   ¦   ¦       tc.png
¦   ¦   ¦       thumbnail.png
¦   ¦   ¦       tiktok.svg
¦   ¦   ¦       title-svg.png
¦   ¦   ¦       upload-icon.png
¦   ¦   ¦       user_welcome.png
¦   ¦   ¦       video-placeholder-gray.png
¦   ¦   ¦       video_1.svg
¦   ¦   ¦       video_ico.svg
¦   ¦   ¦       video_icon.svg
¦   ¦   ¦       video_icon1.svg
¦   ¦   ¦       view.svg
¦   ¦   ¦       youtube.svg
¦   ¦   ¦       
¦   ¦   +---js
¦   ¦           custom.js
¦   ¦           myjs.js
¦   ¦           
¦   +---tc_DigitalMarketing
¦   ¦       asgi.py
¦   ¦       settings.py
¦   ¦       urls.py
¦   ¦       wsgi.py
¦   ¦       __init__.py
¦   ¦       
¦   +---templates
¦       +---email
¦       ¦       activation.html
¦       ¦       admin.html
¦       ¦       approver.html
¦       ¦       creator.html
¦       ¦       default.html
¦       ¦       downloader.html
¦       ¦       
¦       +---tc_DigitalMarketing
¦               activation.html
¦               activationold.html
¦               admin_index.html
¦               approverviewnew copy.html
¦               approverviewnew.html
¦               approver_index.html
¦               createrUploadbase.html
¦               creator.html
¦               css.html
¦               daccess.html
¦               dashboardbase.html
¦               dash_index.html
¦               detailedreport.html
¦               Download.html
¦               downloadaccesspage.html
¦               downloadaccesspageold.html
¦               downloaderview.html
¦               error.html
¦               filterpage.html
¦               index.html
¦               js.html
¦               Login.html
¦               messages.html
¦               myvideos.html
¦               signup.html
¦               statusview.html
¦               TES.HTML
¦               update.html
¦               upload-page copy.html
¦               upload-page.html
¦               upload-page1.html
¦               upload-page1old.html
¦               upload-pagenew.html
¦               uploadagainnew.html
¦               
+---nginx
        default.conf
        Dockerfile
        
```

