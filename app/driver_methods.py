# {
#     "Name": "String(Methods_Name)",
#     "Desc": [ "String(Description)" ],
#     "Args": { Dict({ arg_key:arg_desc }) },
#     "Usage": "String(Usage)"
# }

METHODS = [
    {
        "Name": "activate_ime_engine(self, engine)",
        "Desc": [
            "Activates the given IME engine on the device.",
            "Android only."
        ],
        "Args": {
            "engine": "the package and activity of the IME engine to activate (e.g. 'com.android.inputmethod.latin/.LatinIME')"
        }
    },

    {
        "Name": "app_strings(self, language=None, string_file=None)",
        "Desc": [
            "Returns the application strings from the device for the specified language."
        ],
        "Args": {
            "language": "strings language code",
            "string_file": "the name of the string file to query"
        }
    },

    {
        "Name": "background_app(self, seconds)",
        "Desc": [
            "Puts the application in the background on the device for a certain duration"
        ],
        "Args": {
            "seconds": "the duration for the application to remain in the background"
        }
    },

    {
        "Name": "close_app(self)",
        "Desc": [
            "Stop the running application, specified in the desired capabilities, on the device."
        ]
    },

    {
        "Name": "create_web_element(self, element_id)",
        "Desc": [
            "Creates a web element with the specified element_id.",
            "Overrides method in Selenium WebDriver in order to always give",
            "them Appium WebElement"
        ]
    },

    {
        "Name": "deactivate_ime_engine(self)",
        "Desc": [
            "Deactivates the currently active IME engine on the device.",
            "Android only."
        ]
    },

    {
        "Name": "drag_and_drop(self, origin_el, destination_el)",
        "Desc": [
            "Drag the origin element to the destination element"
        ],
        "Args": {
            "originEl": "the element to drag",
            "destinationEl": "the element to drag to"
        }
    },

    {
        "Name": "end_test_coverage(self, intent, path)",
        "Desc": [
            "Ends the coverage collection and pull the coverage.ec file from the device.",
            "Android only.",
            "See https://github.com/appium/appium/blob/master/docs/en/android_coverage.md"
        ],
        "Args": {
            "intent": "description of operation to be performed",
            "path": "path to coverage.ec file to be pulled from the device"
        }
    },

    {
        "Name": "find_element_by_accessibility_id(self, id)",
        "Desc": [
            "Finds an element by accessibility id."
        ],
        "Args": {
            "id": "a string corresponding to a recursive element search using the Id/Name that the native Accessibility options utilize"
        },
        "Usage": "driver.find_element_by_accessibility_id('accessibility_id')"
    },

    {
        "Name": "find_element_by_android_uiautomator(self, uia_string)",
        "Desc": [
            "Finds element by uiautomator in Android."
        ],
        "Args": {
            "uia_string": "The element name in the Android UIAutomator library"
        },
        "Usage": "driver.find_element_by_android_uiautomator('.elements()[1].cells()[2]')"
    },

    {
        "Name": "find_element_by_ios_predicate(self, predicate_string)",
        "Desc": [
            "Find an element by ios predicate string."
        ],
        "Args": {
            "predicate_string": "The predicate string"
        },
        "Usage": "driver.find_element_by_ios_predicate('label == myLabel')"
    },

    {
        "Name": "find_element_by_ios_uiautomation(self, uia_string)",
        "Desc": [
            "Finds an element by uiautomation in iOS."
        ],
        "Args": {
            "uia_string": "The element name in the iOS UIAutomation library"
        },
        "Usage": "driver.find_element_by_ios_uiautomation('.elements()[1].cells()[2]')"
    },

    {
        "Name": "find_elements_by_accessibility_id(self, id)",
        "Desc": [
            "Finds elements by accessibility id."
        ],
        "Args": {
            "id": "a string corresponding to a recursive element search using the Id/Name that the native Accessibility options utilize"
        },
        "Usage": "driver.find_elements_by_accessibility_id()"
    },

    {
        "Name": "find_elements_by_android_uiautomator(self, uia_string)",
        "Desc": [
            "Finds elements by uiautomator in Android."
        ],
        "Args": {
            "uia_string": "The element name in the Android UIAutomator library"
        },
        "Usage": "driver.find_elements_by_android_uiautomator('.elements()[1].cells()[2]')"

    },

    {
        "Name": "find_elements_by_ios_predicate(self, predicate_string)",
        "Desc": [
            "Finds elements by ios predicate string."
        ],
        "Args": {
            "predicate_string": "The predicate string"
        },
        "Usage": "driver.find_elements_by_ios_predicate(label == 'myLabel')"
    },

    {
        "Name": "find_elements_by_ios_uiautomation(self, uia_string)",
        "Desc": [
            "Finds elements by uiautomation in iOS."
        ],
        "Args": {
            "uia_string": "The element name in the iOS UIAutomation library"
        },
        "Usage": "driver.find_elements_by_ios_uiautomation('.elements()[1].cells()[2]')"
    },

    {
        "Name": "flick(self, start_x, start_y, end_x, end_y)",
        "Desc": [
            "Flick from one point to another point."
        ],
        "Args": {
            "start_x": "x-coordinate at which to start",
            "start_y": "y-coordinate at which to start",
            "end_x": "x-coordinate at which to stop",
            "end_y": "y-coordinate at which to stop"
        },
        "Usage": "driver.flick(100, 100, 100, 400)"
    },

    {
        "Name": "get_settings(self)",
        "Desc": [
            "Returns the appium server Settings for the current session.",
            "Do not get Settings confused with Desired Capabilities, they are",
            "separate concepts. See https://github.com/appium/appium/blob/master/docs/en/advanced-concepts/settings.md"
        ]
    },

    {
        "Name": "hide_keyboard(self, key_name=None, key=None, strategy=None)",
        "Desc": [
            "Hides the software keyboard on the device. In iOS, use 'key_name' to press",
            "a particular key, or 'strategy'. In Android, no parameters are used."
        ],
        "Args": {
            "key_name": "key to press",
            "strategy": "strategy for closing the keyboard (e.g., 'tapOutside')"
        }
    },

    {
        "Name": "install_app(self, app_path)",
        "Desc": [
            "Install the application found at 'app_path' on the device."
        ],
        "Args": {
            "app_path": "the local or remote path to the application to install"
        }
    },

    {
        "Name": "is_app_installed(self, bundle_id)",
        "Desc": [
            "Checks whether the application specified by 'bundle_id' is installed",
            "on the device."
        ],
        "Args": {
            "bundle_id": "the id of the application to query"
        }
    },

    {
        "Name": "is_ime_active(self)",
        "Desc": [
            "Checks whether the device has IME service active. Returns True/False.",
            "Android only."
        ]
    },

    {
        "Name": "keyevent(self, keycode, metastate=None)",
        "Desc": [
            "Sends a keycode to the device. Android only. Possible keycodes can be",
            "found in http://developer.android.com/reference/android/view/KeyEvent.html."
        ],
        "Args": {
            "keycode": "the keycode to be sent to the device",
            "metastate": "meta information about the keycode being sent"
        }
    },

    {
        "Name": "launch_app(self)",
        "Desc": [
            "Start on the device the application specified in the desired capabilities."
        ]
    },

    {
        "Name": "lock(self, seconds)",
        "Desc": [
            "Lock the device for a certain period of time. iOS only."
        ],
        "Args": {
            "seconds": "the duration to lock the device, in seconds"
        }
    },

    {
        "Name": "long_press_keycode(self, keycode, metastate=None)",
        "Desc": [
            "Sends a long press of keycode to the device. Android only. Possible keycodes can be",
            "found in http://developer.android.com/reference/android/view/KeyEvent.html."
        ],
        "Args": {
            "keycode": "the keycode to be sent to the device",
            "metastate": "meta information about the keycode being sent"
        }
    },

    {
        "Name": "open_notifications(self)",
        "Desc": [
            "Open notification shade in Android (API Level 18 and above)"
        ]
    },

    {
        "Name": "pinch(self, element=None, percent=200, steps=50)",
        "Desc": [
            "Pinch on an element a certain amount"
        ],
        "Args": {
            "element": "the element to pinch",
            "percent": "(optional) amount to pinch. Defaults to 200%",
            "steps": "(optional) number of steps in the pinch action"
        },
        "Usage": "driver.pinch(element)"
    },

    {
        "Name": "press_keycode(self, keycode, metastate=None)",
        "Desc": [
            "Sends a keycode to the device. Android only. Possible keycodes can be",
            "found in http://developer.android.com/reference/android/view/KeyEvent.html."
        ],
        "Args": {
            "keycode": "the keycode to be sent to the device",
            "metastate": "meta information about the keycode being sent"
        }
    },

    {
        "Name": "pull_file(self, path)",
        "Desc": [
            "Retrieves the file at 'path'. Returns the file's content encoded as",
            "Base64."
        ],
        "Args": {
            "path": "the path to the file on the device"
        }
    },

    {
        "Name": "pull_folder(self, path)",
        "Desc": [
            "Retrieves a folder at 'path'. Returns the folder's contents zipped",
            "and encoded as Base64."
        ],
        "Args": {
            "path": "the path to the folder on the device"
        }
    },

    {
        "Name": "push_file(self, path, base64data)",
        "Desc": [
            "Puts the data, encoded as Base64, in the file specified as 'path'."
        ],
        "Args": {
            "path": "the path on the device",
            "base64data": "data, encoded as Base64, to be written to the file"
        }
    },

    {
        "Name": "remove_app(self, app_id)",
        "Desc": [
            "Remove the specified application from the device."
        ],
        "Args": {
            "app_id": "the application id to be removed"
        }
    },

    {
        "Name": "reset(self)",
        "Desc": [
            "Resets the current application on the device."
        ]
    },

    {
        "Name": "scroll(self, origin_el, destination_el)",
        "Desc": [
            "Scrolls from one element to another"
        ],
        "Args": {
            "originalEl": "the element from which to being scrolling",
            "destinationEl": "the element to scroll to"
        },
        "Usage": "driver.scroll(el1, el2)"
    },

    {
        "Name": "set_location(self, latitude, longitude, altitude)",
        "Desc": [
            "Set the location of the device"
        ],
        "Args": {
            "latitude": "String or numeric value between -90.0 and 90.00",
            "longitude": "String or numeric value between -180.0 and 180.0",
            "altitude": "String or numeric value"
        }
    },

    {
        "Name": "set_network_connection(self, connectionType)",
        "Desc": [
            "Sets the network connection type. Android only.",
            "Possible values:",
            "Value (Alias)      | Data | Wifi | Airplane Mode",
            "-------------------------------------------------",
            "0 (None)           | 0    | 0    | 0",
            "1 (Airplane Mode)  | 0    | 0    | 1",
            "2 (Wifi only)      | 0    | 1    | 0",
            "4 (Data only)      | 1    | 0    | 0",
            "6 (All network on) | 1    | 1    | 0",
            "These are available through the enumeration 'appium.webdriver.ConnectionType'"
        ],
        "Args": {
            "connectionType": "a member of the enum appium.webdriver.ConnectionType"
        }
    },

    {
        "Name": "set_value(self, element, value)",
        "Desc": [
            "Set the value on an element in the application."
        ],
        "Args": {
            "element": "the element whose value will be set",
            "Value": "the value to set on the element"
        }
    },

    {
        "Name": "shake(self)",
        "Desc": [
            "Shake the device."
        ]
    },

    {
        "Name": "start_activity(self, app_package, app_activity, **opts)",
        "Desc": [
            "Opens an arbitrary activity during a test. If the activity belongs to",
            "another application, that application is started and the activity is opened.",
            "This is an Android-only method."
        ],
        "Args": {
            "app_package": "The package containing the activity to start.",
            "app_activity": "The activity to start.",
            "app_wait_package": "Begin automation after this package starts (optional).",
            "app_wait_activity": "Begin automation after this activity starts (optional).",
            "intent_action": "Intent to start (optional).",
            "intent_category": "Intent category to start (optional).",
            "intent_flags": "Flags to send to the intent (optional).",
            "optional_intent_arguments": "Optional arguments to the intent (optional).",
            "dont_stop_app_on_reset": "Should the app be stopped on reset (optional)?"
        }
    },

    {
        "Name": "swipe(self, start_x, start_y, end_x, end_y, duration=None)",
        "Desc": [
            "Swipe from one point to another point, for an optional duration."
        ],
        "Args": {
            "start_x": "x-coordinate at which to start",
            "start_y": "y-coordinate at which to start",
            "end_x": "x-coordinate at which to stop",
            "end_y": "y-coordinate at which to stop",
            "duration": "(optional) time to take the swipe, in ms."
        },
        "Usage": "driver.swipe(100, 100, 100, 400)"
    },

    {
        "Name": "tap(self, positions, duration=None)",
        "Desc": [
            "Taps on an particular place with up to five fingers, holding for a certain time"
        ],
        "Args": {
            "positions": "an array of tuples representing the x/y coordinates of the fingers to tap. Length can be up to five.",
            "duration": "(optional) length of time to tap, in ms"
        },
        "Usage": "driver.tap([(100, 20), (100, 60), (100, 100)], 500)"
    },

    {
        "Name": "toggle_location_services(self)",
        "Desc": [
            "Toggle the location services on the device. Android only."
        ],
        "Usage": ""
    },

    {
        "Name": "touch_id(self, match)",
        "Desc": [
            "Do a fingerprint scan"
        ]
    },

    {
        "Name": "update_settings(self, settings)",
        "Desc": [
            "Set settings for the current session.",
            "For more on settings, see: https://github.com/appium/appium/blob/master/docs/en/advanced-concepts/settings.md"
        ],
        "Args": {
            "settings": "dictionary of settings to apply to the current test session"
        }
    },

    {
        "Name": "wait_activity(self, activity, timeout, interval=1)",
        "Desc": [
            "Wait for an activity: block until target activity presents or time out.",
            "This is an Android-only method."
        ],
        "Args": {
            "activity": "target activity",
            "timeout": "max wait time, in seconds",
            "interval": "sleep interval between retries, in seconds"
        }
    },

    {
        "Name": "zoom(self, element=None, percent=200, steps=50)",
        "Desc": [
            "Zooms in on an element a certain amount"
        ],
        "Args": {
            "element": "the element to zoom",
            "percent": "(optional) amount to zoom. Defaults to 200%",
            "steps": "(optional) number of steps in the zoom action"
        },
        "Usage": "driver.zoom(element)"
    },




    #  ----------------------------------------------------------------------
    #  Methods inherited from selenium.webdriver.remote.webdriver.WebDriver:
     #
    #  __repr__(self)

    {
        "Name": "add_cookie(self, cookie_dict)",
        "Desc": [
            "Adds a cookie to your current session."
        ],
        "Args": {
            "cookie_dict": "A dictionary object, with required keys 'name' and 'value' optional keys 'path', 'domain', 'secure', 'expiry'"
        },
        "Usage": "driver.add_cookie({'name' : 'foo', 'value' : 'bar', 'path' : '/', 'secure':True})"
    },

    {
        "Name": "back(self)",
        "Desc": [
            "Goes one step backward in the browser history."
        ],
        "Usage": "driver.back()"
    },

    {
        "Name": "close(self)",
        "Desc": [
            "Closes the current window."
        ],
        "Usage": "driver.close()"
    },

    {
        "Name": "delete_all_cookies(self)",
        "Desc": [
            "Delete all cookies in the scope of the session."
        ],
        "Usage": "driver.delete_all_cookies()"
    },

    {
        "Name": "delete_cookie(self, name)",
        "Desc": [
            "Deletes a single cookie with the given name."
        ],
        "Usage": "driver.delete_cookie('my_cookie')"
    },

    {
        "Name": "execute(self, driver_command, params=None)",
        "Desc": [
            "Sends a command to be executed by a command.CommandExecutor."
        ],
        "Args": {
            "driver_command": "The name of the command to execute as a string.",
            "params": "A dictionary of named parameters to send with the command."
        }
    },

    {
        "Name": "execute_async_script(self, script, *args)",
        "Desc": [
            "Asynchronously Executes JavaScript in the current window/frame."
        ],
        "Args": {
            "script": "The JavaScript to execute.",
            "*args": "Any applicable arguments for your JavaScript."
        },
        "Usage": "driver.execute_async_script('document.title')"
    },

    {
        "Name": "execute_script(self, script, *args)",
        "Desc": [
            "Synchronously Executes JavaScript in the current window/frame."
        ],
        "Args": {
            "script": "The JavaScript to execute.",
            "*args": "Any applicable arguments for your JavaScript."
        },
        "Usage": "driver.execute_script('document.title')"
    },

    {
        "Name": "file_detector_context(*args, **kwds)",
        "Desc": [
            "Overrides the current file detector (if necessary) in limited context.",
            "Ensures the original file detector is set afterwards."
        ],
        "Args": {
            "file_detector_class": "Class of the desired file detector. If the class is different from the current file_detector, then the class is instantiated with args and kwargs and used as a file detector during the duration of the context manager.",
            "Args": "Optional arguments that get passed to the file detector class during instantiation.",
            "kwargs": "Keyword arguments, passed the same way as args."
        },
        "Usage": ""
    },

    {
        "Name": "find_element(self, by='id', value=None)",
        "Desc": [
            "'Private' method used by the find_element_by_* methods."
        ],
        "Usage": "Use the corresponding find_element_by_* instead of this."
    },

    {
        "Name": "find_element_by_class_name(self, name)",
        "Desc": [
            "Finds an element by class name."
        ],
        "Args": {
            "Name": "The class name of the element to find."
        },
        "Usage": "driver.find_element_by_class_name('foo')"
    },

    {
        "Name": "find_element_by_css_selector(self, css_selector)",
        "Desc": [
            "Finds an element by css selector."
        ],
        "Args": {
            "css_selector": "The css selector to use when finding elements."
        },
        "Usage": "driver.find_element_by_css_selector('#foo')"
    },

    {
        "Name": "find_element_by_id(self, id_)",
        "Desc": [
            "Finds an element by id."
        ],
        "Args": {
            "id_": "The id of the element to be found."
        },
        "Usage": "driver.find_element_by_id('foo')"
    },

    {
        "Name": "find_element_by_link_text(self, link_text)",
        "Desc": [
            "Finds an element by link text."
        ],
        "Args": {
            "link_text": "The text of the element to be found."
        },
        "Usage": "driver.find_element_by_link_text('Sign In')"
    },

    {
        "Name": "find_element_by_name(self, name)",
        "Desc": [
            "Finds an element by name."
        ],
        "Args": {
            "Name": "The name of the element to find."
        },
        "Usage": "driver.find_element_by_name('foo')"
    },

    {
        "Name": "find_element_by_partial_link_text(self, link_text)",
        "Desc": [
            "Finds an element by a partial match of its link text."
        ],
        "Args": {
            "link_text": "The text of the element to partially match on."
        },
        "Usage": "driver.find_element_by_partial_link_text('Sign')"
    },

    {
        "Name": "find_element_by_tag_name(self, name)",
        "Desc": [
            "Finds an element by tag name."
        ],
        "Args": {
            "Name": "The tag name of the element to find."
        },
        "Usage": "driver.find_element_by_tag_name('foo')"
    },

    {
        "Name": "find_element_by_xpath(self, xpath)",
        "Desc": [
            "Finds an element by xpath."
        ],
        "Args": {
            "xpath": "The xpath locator of the element to find."
        },
        "Usage": "driver.find_element_by_xpath('//div/td[1]')"
    },

    {
        "Name": "find_elements(self, by='id', value=None)",
        "Desc": [
            "'Private' method used by the find_elements_by_* methods."
        ],
        "Usage": "Use the corresponding find_elements_by_* instead of this."
    },


    {
        "Name": "find_elements_by_class_name(self, name)",
        "Desc": [
            "Finds elements by class name."
        ],
        "Args": {
            "Name": "The class name of the elements to find."
        },
        "Usage": "driver.find_elements_by_class_name('foo')"
    },

    {
        "Name": "find_elements_by_css_selector(self, css_selector)",
        "Desc": [
            "Finds elements by css selector."
        ],
        "Args": {
            "css_selector": "The css selector to use when finding elements."
        },
        "Usage": "driver.find_elements_by_css_selector('.foo')"
    },

    {
        "Name": "find_elements_by_id(self, id_)",
        "Desc": [
            "Finds multiple elements by id."
        ],
        "Args": {
            "id_": "The id of the elements to be found."
        },
        "Usage": "driver.find_elements_by_id('foo')"
    },

    {
        "Name": "find_elements_by_link_text(self, text)",
        "Desc": [
            "Finds elements by link text."
        ],
        "Args": {
            "link_text": "The text of the elements to be found."
        },
        "Usage": "driver.find_elements_by_link_text('Sign In')"
    },

    {
        "Name": "find_elements_by_name(self, name)",
        "Desc": [
            "Finds elements by name."
        ],
        "Args": {
            "Name": "The name of the elements to find."
        },
        "Usage": "driver.find_elements_by_name('foo')"
    },

    {
        "Name": "find_elements_by_partial_link_text(self, link_text)",
        "Desc": [
            "Finds elements by a partial match of their link text."
        ],
        "Args": {
            "link_text": "The text of the element to partial match on."
        },
        "Usage": "driver.find_element_by_partial_link_text('Sign')"
    },

    {
        "Name": "find_elements_by_tag_name(self, name)",
        "Desc": [
            "Finds elements by tag name."
        ],
        "Args": {
            "Name": "The tag name the use when finding elements."
        },
        "Usage": "driver.find_elements_by_tag_name('foo')"
    },

    {
        "Name": "find_elements_by_xpath(self, xpath)",
        "Desc": [
            "Finds multiple elements by xpath."
        ],
        "Args": {
            "xpath": "The xpath locator of the elements to be found."
        },
        "Usage": "driver.find_elements_by_xpath('//div[contains(@class, 'foo')]')"
    },

    {
        "Name": "forward(self)",
        "Desc": [
            "Goes one step forward in the browser history."
        ],
        "Usage": "driver.forward()"
    },

    {
        "Name": "get(self, url)",
        "Desc": [
            "Loads a web page in the current browser session."
        ]
    },

    {
        "Name": "get_cookie(self, name)",
        "Desc": [
            "Get a single cookie by name. Returns the cookie if found, None if not."
        ],
        "Usage": "driver.get_cookie('my_cookie')"
    },

    {
        "Name": "get_cookies(self)",
        "Desc": [
            "Returns a set of dictionaries, corresponding to cookies visible in the current session."
        ],
        "Usage": "driver.get_cookies()"
    },

    {
        "Name": "get_log(self, log_type)",
        "Desc": [
            "Gets the log for a given log type"
        ],
        "Args": {
            "log_type": "type of log that which will be returned"
        },
        "Usage": "driver.get_log('browser') | driver.get_log('driver') | driver.get_log('client') | driver.get_log('server')"
    },

    {
        "Name": "get_screenshot_as_base64(self)",
        "Desc": [
            "Gets the screenshot of the current window as a base64 encoded string",
            "which is useful in embedded images in HTML."
        ],
        "Usage": "driver.get_screenshot_as_base64()"
    },

    {
        "Name": "get_screenshot_as_file(self, filename)",
        "Desc": [
            "Gets the screenshot of the current window. Returns False if there is",
            "any IOError, else returns True. Use full paths in your filename."
        ],
        "Args": {
            "filename": "The full path you wish to save your screenshot to."
        },
        "Usage": "driver.get_screenshot_as_file('/Screenshots/foo.png')"
    },

    {
        "Name": "get_screenshot_as_png(self)",
        "Desc": [
            "Gets the screenshot of the current window as a binary data."
        ],
        "Usage": "driver.get_screenshot_as_png()"
    },

    {
        "Name": "get_window_position(self, windowHandle='current')",
        "Desc": [
            "Gets the x,y position of the current window."
        ],
        "Usage": "driver.get_window_position()"
    },

    {
        "Name": "get_window_rect(self)",
        "Desc": [
            "Gets the x, y coordinates of the window as well as height and width of",
            "the current window."
        ],
        "Usage": "driver.get_window_rect()"
    },

    {
        "Name": "get_window_size(self, windowHandle='current')",
        "Desc": [
            "Gets the width and height of the current window."
        ],
        "Usage": "driver.get_window_size()"
    },

    {
        "Name": "implicitly_wait(self, time_to_wait)",
        "Desc": [
            "Sets a sticky timeout to implicitly wait for an element to be found,",
            "or a command to complete. This method only needs to be called one",
            "time per session. To set the timeout for calls to",
            "execute_async_script, see set_script_timeout."
        ],
        "Args": {
            "time_to_wait": "Amount of time to wait (in seconds)"
        },
        "Usage": "driver.implicitly_wait(30)"
    },

    {
        "Name": "maximize_window(self)",
        "Desc": [
            "Maximizes the current window that webdriver is using"
        ]
    },

    {
        "Name": "quit(self)",
        "Desc": [
            "Quits the driver and closes every associated window."
        ],
        "Usage": "driver.quit()"
    },

    {
        "Name": "refresh(self)",
        "Desc": [
            "Refreshes the current page."
        ],
        "Usage": "driver.refresh()"
    },

    {
        "Name": "save_screenshot(self, filename)",
        "Desc": [
            "Gets the screenshot of the current window. Returns False if there is",
            "any IOError, else returns True. Use full paths in your filename."
        ],
        "Args": {
            "filename": "The full path you wish to save your screenshot to."
        },
        "Usage": "driver.save_screenshot('/Screenshots/foo.png')"
    },

    {
        "Name": "set_page_load_timeout(self, time_to_wait)",
        "Desc": [
            "Set the amount of time to wait for a page load to complete",
            "before throwing an error."
        ],
        "Args": {
            "time_to_wait": "The amount of time to wait"
        },
        "Usage": "driver.set_page_load_timeout(30)"
    },

    {
        "Name": "set_script_timeout(self, time_to_wait)",
        "Desc": [
            "Set the amount of time that the script should wait during an",
            "execute_async_script call before throwing an error."
        ],
        "Args": {
            "time_to_wait": "The amount of time to wait (in seconds)"
        },
        "Usage": "driver.set_script_timeout(30)"
    },

    {
        "Name": "set_window_position(self, x, y, windowHandle='current')",
        "Desc": [
            "Sets the x,y position of the current window. (window.moveTo)"
        ],
        "Args": {
            "x": "the x-coordinate in pixels to set the window position",
            "y": "the y-coordinate in pixels to set the window position"
        },
        "Usage": "driver.set_window_position(0,0)"
    },

    {
        "Name": "set_window_rect(self, x=None, y=None, width=None, height=None)",
        "Desc": [
            "Sets the x, y coordinates of the window as well as height and width of",
            "the current window."
        ],
        "Usage": "driver.set_window_rect(x=10, y=10) | driver.set_window_rect(width=100, height=200) | driver.set_window_rect(x=10, y=10, width=100, height=200)"
    },

    {
        "Name": "set_window_size(self, width, height, windowHandle='current')",
        "Desc": [
            "Sets the width and height of the current window. (window.resizeTo)"
        ],
        "Args": {
            "width": "the width in pixels to set the window to",
            "height": "the height in pixels to set the window to"
        },
        "Usage": "driver.set_window_size(800,600)"
    },

    {
        "Name": "start_client(self)",
        "Desc": [
            "Called before starting a new session. This method may be overridden",
            "to define custom startup behavior."
        ]
    },

    {
        "Name": "start_session(self, capabilities, browser_profile=None)",
        "Desc": [
            "Creates a new session with the desired capabilities."
        ],
        "Args": {
            "browser_name": "The name of the browser to request.",
            "version": "Which browser version to request.",
            "platform": "Which platform to request the browser on.",
            "javascript_enabled": "Whether the new session should support JavaScript.",
            "browser_profile": "A selenium.webdriver.firefox.firefox_profile.FirefoxProfile object. Only used if Firefox is requested."
        }
    },

    {
        "Name": "stop_client(self)",
        "Desc": [
            "Called after executing a quit command. This method may be overridden",
            "to define custom shutdown behavior."
        ]
    },

    {
        "Name": "switch_to_active_element(self)",
        "Desc": [
            "Deprecated use driver.switch_to.active_element"
        ]
    },

    {
        "Name": "switch_to_alert(self)",
        "Desc": [
            "Deprecated use driver.switch_to.alert"
        ]
    },

    {
        "Name": "switch_to_default_content(self)",
        "Desc": [
            "Deprecated use driver.switch_to.default_content"
        ]
    },

    {
        "Name": "switch_to_frame(self, frame_reference)",
        "Desc": [
            "Deprecated use driver.switch_to.frame"
        ]
    },

    {
        "Name": "switch_to_window(self, window_name)",
        "Desc": [
            "Deprecated use driver.switch_to.window"
        ]
    },

    # ----------------------------------------------------------------------
    # Data descriptors defined here:

    {
        "Name": "active_ime_engine",
        "Desc": [
            "Returns the activity and package of the currently active IME engine (e.g.'com.android.inputmethod.latin/.LatinIME').",
            "Android only."
        ]
    },

    {
        "Name": "available_ime_engines",
        "Desc": [
            "Get the available input methods for an Android device. Package and",
            "activity are returned (e.g., ['com.android.inputmethod.latin/.LatinIME'])",
            "Android only."
        ]
    },

    {
        "Name": "context",
        "Desc": [
            "Returns the current context of the current session."
        ],
        "Usage": "driver.context"
    },

    {
        "Name": "contexts",
        "Desc": [
            "Returns the contexts within the current session."
        ],
        "Usage": "driver.contexts"
    },

    {
        "Name": "current_activity",
        "Desc": [
            "Retrieves the current activity on the device."
        ],
        "Usage": "driver.current_activity"
    },

    {
        "Name": "current_context",
        "Desc": [
            "Returns the current context of the current session."
        ],
        "Usage": "driver.current_context"
    },

    {
        "Name": "device_time",
        "Desc": [
            "Returns the date and time fomr the device"
        ],
        "Usage": "driver.device_time"
    },

    {
        "Name": "network_connection",
        "Desc": [
            "Returns an integer bitmask specifying the network connection type.",
            "Android only.",
            "Possible values are available through the enumeration 'appium.webdriver.ConnectionType'"
        ],
        "Usage": "driver.network_connection"
    },

    #  ----------------------------------------------------------------------
    #  Data descriptors inherited from selenium.webdriver.remote.webdriver.WebDriver:
     #
    #  __dict__
    #      dictionary for instance variables (if defined)
     #
    #  __weakref__
    #      list of weak references to the object (if defined)


    {
        "Name": "application_cache",
        "Desc": [
            "Returns a ApplicationCache Object to interact with the browser app cache"
        ]
    },

    {
        "Name": "current_url",
        "Desc": [
            "Gets the URL of the current page."
        ],
        "Usage": "driver.current_url"
    },

    {
        "Name": "current_window_handle",
        "Desc": [
            "Returns the handle of the current window."
        ],
        "Usage": "driver.current_window_handle"
    },

    {
        "Name": "desired_capabilities",
        "Desc": [
            "returns the drivers current desired capabilities being used"
        ]
    },

    {
        "Name": "file_detector"
    },

    {
        "Name": "log_types",
        "Desc": [
            "Gets a list of the available log types"
        ],
        "Usage": "driver.log_types"
    },

    {
        "Name": "mobile"
    },

    {
        "Name": "Name",
        "Desc": [
            "Returns the name of the underlying browser for this instance."
        ],
        "Usage": "driver.name"
    },

    {
        "Name": "orientation",
        "Desc": [
            "Gets the current orientation of the device"
        ],
        "Usage": "driver.orientation"
    },

    {
        "Name": "page_source",
        "Desc": [
            "Gets the source of the current page."
        ],
        "Usage": "driver.page_source"
    },

    {
        "Name": "switch_to"
    },

    {
        "Name": "title",
        "Desc": [
            "Returns the title of the current page."
        ],
        "Usage": "driver.title"
    },

    {
        "Name": "window_handles",
        "Desc": [
            "Returns the handles of all windows within the current session."
        ],
        "Usage": "driver.window_handles"
    }
]
