# Appium-Python-Console


## 1. Appium Desktop Download
Link : [http://appium.io/]

1) 위 링크로 이동

2) Download Appium 을 통해 Appium Desktop download 페이지로 이동

3) Appium Desktop 파일 다운 로드 후 실행




## 2. Appium Github Clone

Link : [https://github.com/appium/appium]

1) Git을 이용하여 Appium Project Clone
```
git clone https://github.com/appium/appium.git﻿﻿
```

2) Clone 한 Appium 폴더로 이동
```
cd appium
```

3) NPM Install
```
npm install
```

4) Appium 실행 [ node .(dot) ]
```
node .

# 아래와 같은 메세지가 출력 되면 Appium 실행 완료
[Appium] Welcome to Appium v1.7.0-beta (REV cf24a80809309fb5467099e570cddd256cacbb28)
[Ap﻿pium] Appium REST http interface listener started on 0.0.0.0:4723
```

```
// Error Case 1 :
module.js:491
    throw err;
    ^

Error: Cannot find module '/Users/han/Documents/appium-1.6.5'
    at Function.Module._resolveFilename (module.js:489:15)
    at Function.Module._load (module.js:439:25)
    at Function.Module.runMain (module.js:609:10)
    at startup (bootstrap_node.js:158:16)
    at bootstrap_node.js:598:3

// Error Case 2 :
npm install 실행 후 Appium 프로젝트 폴더에 build 라는 폴더가 있는지 확인 없을 경우 다음 명령줄 실행

# 해결법 : 다음 명령줄 실행

sudo xcode-select --switch /Library/Developer/CommandLineTools
```



## 3. Appium Github Release Download

Link : [https://github.com/appium/appium/releases]

1) 위 링크에서 원하는 버전의 Appium 압축 파일 다운로드

2) 압축풀기
```
cd PATH/TO/DOWNLOAD/FOLDER

// tar.gz 압축풀기 명령어
tar -zxvf appium-1.6.x.tar.gz TARGET/PATH

ex) tar -zxvf appium-1.6.3.tar.gz ~/Documents/appium-1.6.3
```

3) 해당 폴더로 이동

```
cd appium-1.6.3
```

4) NPM Install

```
npm install
```

5) Appium 실행 [ node .(dot) ]

```
node .
```
