# Appium-Python-Console


## 1. Appium Desktop Download
-----------------------------

## 2. Appium Github Clone
-------------------------

Link : [https://github.com/appium/appium][https://github.com/appium/appium]

* Git을 이용하여 Appium Project Clone
```
git clone https://github.com/appium/appium.git﻿﻿
```

* Clone 한 Appium 폴더로 이동
```
cd appium
```

* NPM Install
```
npm install
```

* Appium 실행 [ node .(dot) ]
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
------------------------------------
