function getXPath(node) {
    var comp, comps = [];
    var parent = null;
    var xpath = "";
    var hostname = window.location.hostname;
    var pathName = window.location.pathname;

    var getAndroidComp = function(name) {
        if (name.toUpperCase() == "HTML") {
            return "HTML";
        } else if (name.toUpperCase() == "BODY") {
            return "BODY";
        } else if (name.toUpperCase() == "HEAD") {
            return "HEAD";
        } else if (name.toUpperCase() == "SCRIPT") {
            return "SCRIPT";
        } else if (name.toUpperCase() == "UL") {
            return "ListView";
        } else {
            return "View";
        }
    };

    var isDisplayed = function(node) {
        if (node.style.display == "none") {
            return false;
        }
        if (node.hasAttribute("type") && node.getAttribute("type") == "hidden") {
            return false;
        }
        if (node.hasAttribute("id")) {
            return true;
        }
        if (node.offsetHeight == 0) {
            return false;
        }
        return true;
    }

    var getPos = function(node) {
        var position = 1,
            curNode;
        if (node.nodeType == Node.ATTRIBUTE_NODE) {
            return null;
        }
        for (curNode = node.previousSibling; curNode; curNode = curNode.previousSibling) {
            if (curNode.nodeName == node.nodeName) {
                ++position;
            }
        }
        return position;
    };

    if (node instanceof Document) {
        return "/";
    }

    for (; node && !(node instanceof Document); node = node.nodeType == Node.ATTRIBUTE_NODE ? node.ownerElement : node.parentNode) {
        comp = comps[comps.length] = {};
        switch (node.nodeType) {
            case Node.TEXT_NODE:
                comp.name = "text()";
                break;
            case Node.ATTRIBUTE_NODE:
                comp.name = "@" + node.nodeName;
                break;
            case Node.PROCESSING_INSTRUCTION_NODE:
                comp.name = "processing-instruction()";
                break;
            case Node.COMMENT_NODE:
                comp.name = "comment()";
                break;
            case Node.ELEMENT_NODE:
                comp.name = node.nodeName;
                break;
        }
        comp.position = getPos(node);
    }

    for (var i = comps.length - 1; i >= 0; i--) {
        comp = comps[i];
        xpath += "/" + comp.name;
        if (comp.position != null) {
            xpath += "[" + comp.position + "]";
        }
    }

    xpath = '#' + hostname + pathName + ':' + xpath;

    return xpath;
}

function intersect_bouunds_compare(r_el, el) {
    var el_rect = el.getBoundingClientRect();
    var el_b = {
        "left": Math.floor(el_rect.left),
        "top": Math.floor(el_rect.top),
        "right": Math.ceil(el_rect.right),
        "bottom": Math.ceil(el_rect.bottom)
    };
    var el_b_w = el_b.right - el_b.left;
    var el_b_h = el_b.bottom - el_b.top;
    var el_b_area = el_b_w * el_b_h;

    var f_el = r_el.filter(function(item) {
        var item_rect = item.target.getBoundingClientRect();
        var item_b = {
            "left": Math.floor(item_rect.left),
            "top": Math.floor(item_rect.top),
            "right": Math.ceil(item_rect.right),
            "bottom": Math.ceil(item_rect.bottom)
        }

        var item_b_w = item_b.right - item_b.left;
        var item_b_h = item_b.bottom - item_b.top;
        var item_b_area = item_b_w * item_b_h;

        var p1 = [Math.max(el_b.left, item_b.left), Math.max(el_b.top, item_b.top)];
        var p2 = [Math.min(el_b.right, item_b.right), Math.min(el_b.bottom, item_b.bottom)];

        var w = p2[0] - p1[0] > 1 ? p2[0] - p1[0] : 0;
        var h = p2[1] - p1[1] > 1 ? p2[1] - p1[1] : 0;
        var area = w * h;
        if (area > 0 && (el_b_area === area || item_b_area === area)) {
            return item;
        }
    });
    return f_el[0];
}

function check_interect_data_and_set_element(r_el, el, element_data) {
    var f_el_idx = r_el.indexOf(intersect_bouunds_compare(r_el, el));
    if (f_el_idx !== -1) {
        r_el[f_el_idx] = element_data;
    } else {
        r_el.push(element_data);
    }
}


function getMaxElement(node, max) {
    var nodes = node.childNodes;
    for (var i = 0; i < nodes.length; i++) {
        if (nodes[i].childNodes.length) {
            max = getMaxElement(nodes[i], max);
        } else {
            if (nodes[i].offsetHeight >= max.offsetHeight) {
                max = nodes[i];
            }
        }
    }

    return max;
}

function getMaxBounds(node) {
    var maxNode = getMaxElement(node, node);
    return getBounds(maxNode);
}

function getBounds(node) {
    var b = node.getBoundingClientRect();
    bounds = "[" + Math.floor(b.left) + "," + Math.floor(b.top) + "][" + Math.ceil(b.right) + "," + Math.ceil(b.bottom) + "]";
    return bounds;
}

function checkSelectChild(node) {
    var childNodes = node.childNodes;
    var existSelect = false;
    if (node.tagName.toUpperCase() === "SELECT") {
      return true;
    }
    for (var i = 0; i < childNodes.length; i++) {
        if (childNodes[i].tagName && childNodes[i].tagName.toUpperCase() === 'SELECT') {
            existSelect = true;
        }
    }
    return existSelect;
}

function getDesc(node) {
  var desc = checkDesc([node]);
  if (desc !== '') {
    return desc;
  }
	desc = checkDesc(node.childNodes);
  return desc;
}


function checkDesc(node) {
	var nodes = node;
	var desc = '';
	for(var i=0; i < nodes.length; i++) {
    // Select tag Value
    if (nodes[i].tagName.toUpperCase() === 'SELECT' && node[i].selectedOptions && node[i].selectedOptions[0] && node[i].selectedOptions[0].textContent !== '') {
      desc = nodes[i].selectedOptions[0].textContent;
			break;
		}
    // Select tag Value
    if (nodes[i].tagName.toUpperCase() === 'SELECT' && nodes[i].value && nodes[i].value !== '') {
      desc = nodes[i].value;
			break;
		}

    // Input tag Value
    if (nodes[i].tagName.toUpperCase() === 'INPUT' && nodes[i].labels  && nodes[i].labels[0] && nodes[i].labels[0].textContent !== '') {
			desc = nodes[i].labels[0].textContent;
			break;
		}
    // Input tag Value
    if (nodes[i].tagName.toUpperCase() === 'INPUT' && nodes[i].value && nodes[i].value !== '') {
			desc = nodes[i].value.toString();
			break;
		}
    // Input tag Value
    if (nodes[i].tagName.toUpperCase() === 'INPUT' && nodes[i].placeholder && nodes[i].placeholder !== '') {
			desc = nodes[i].placeholder;
			break;
		}
    // TextContent
    if (nodes[i].textContent !== '') {
			desc = nodes[i].textContent;
			break;
		}

    // Icon tag Class Name
		if (nodes[i].firstChild && nodes[i].firstChild.tagName && nodes[i].firstChild.tagName.toUpperCase() === 'I' && nodes[i].firstChild.className) {
			desc = nodes[i].firstChild.className;
			break;
		}
    // Icon tag Class Name
		if (nodes[i].lastChild && nodes[i].firstChild.tagName && nodes[i].lastChild.tagName.toUpperCase() === 'I' && nodes[i].lastChild.className) {
			desc = nodes[i].lastChild.className;
			break;
		}

    // Title attribute
		if (nodes[i].title !== '') {
			desc = nodes[i].title;
			break;
		}
    // Name attribute
		if (nodes[i].hasAttribute("name") && nodes[i].getAttribute("name") !== null) {
			desc = nodes[i].getAttribute("name");
			break;
		}
    // ID attribute
    if (nodes[i].hasAttribute("id") && nodes[i].getAttribute("id") !== null) {
		  desc = nodes[i].getAttribute("id");
		  break;
		}
    // Alt attribute
		if (nodes[i].hasAttribute("alt") && nodes[i].getAttribute("alt") !== null) {
			desc = nodes[i].getAttribute("alt");
			break;
		}
	}
    return desc;
}


function equal_bounds_el_check(r_el, el) {
    var bounds = getMaxBounds(el);
    var f_el = r_el.filter(function(item) {
        return (item.bounds === bounds);
    });

    return f_el.length > 0;
}

function zindex_check(r_el, el) {
    bounds = getMaxBounds(el);
    var f_el = r_el.filter(function(item) {
        return (item.bounds === bounds);
    });

    var f_el_zindex = getComputedStyle(f_el[0].target).zIndex;
    var el_zindex = getComputedStyle(el).zIndex;

    if (f_el_zindex === 'auto' && el_zindex === 'auto') {
        return {
            'reult': true,
            'f_el': f_el
        };
    } else if (f_el_zindex === 'auto' && el_zindex > 0) {
        return {
            'reult': true,
            'f_el': f_el
        };
    } else if (f_el_zindex < el_zindex) {
        return {
            'reult': true,
            'f_el': f_el
        };
    } else {
        return {
            'reult': false,
            'f_el': f_el
        };
    }
}

function get_at_jq() {
    var at_jq = {};
    var i = 0;
    while ($ !== undefined && $.noConflict !== undefined) {
        at_jq['$jq_' + i] = $.noConflict();
        i++;
    }
    return at_jq;
}

function get_at_jq_keys(at_jq) {
    var at_jq_keys = Object.keys(at_jq);
    for (var i = 0; i < at_jq_keys.length; i++) {
        var idx = at_jq_keys.length - i - 1;
        $ = at_jq[at_jq_keys[idx]].noConflict();
    }
    return at_jq_keys;
}


/**
 * Compare two version strings
 *  @static
 *  @param {string} v1 Version 1 string
 *  @param {string} operator '<', '<=', '==', '>=' or '>' - logic operation to
 *    perform
 *  @param {string} v2 Version 2 string
 *  @returns {boolean} true if condition is correct, false otherwise
 */
function versionCompare(v1, operator, v2) {
    var a1 = v1.split('.');
    var a2 = v2.split('.');
    var i1, i2;
    var test = 0;

    for (var i = 0, iLen = a2.length; i < iLen; i++) {
        i1 = parseInt(a1[i], 10) || 0;
        i2 = parseInt(a2[i], 10) || 0;

        // Parts are the same, keep comparing
        if (i1 < i2) {
            test = -1;
            break;
        } else if (i1 > i2) {
            test = 1;
            break;
        }
    }

    if (operator === '<') {
        return test === -1;
    } else if (operator === '<=') {
        return test === -1 || test === 0;
    } else if (operator === '==') {
        return test === 0;
    } else if (operator === '>=') {
        return test === 0 || test === 1;
    } else if (operator === '>') {
        return test === 1;
    }
    throw 'Unknown operator: ' + operator;
};


function set_element_data(el, inputType, action, type, className, el_id) {
    var input_type = check_child_tag_name(el);
    return {
        "target": el,
        "input-type": input_type["input_type"] !== null ? input_type["input_type"] : inputType,
        "checked": input_type["checked"] !== null ? input_type["checked"] : ( el.checked === undefined ? 'false' : el.checked.toString() ),
        "action": action,
        "xpath": getXPath(el),
        "bounds": getMaxBounds(el),
        "content-desc": getDesc(el).trim().slice(0, 15).replace(/\t/g, '').replace(/\n/g, '').trim(),
        "type": input_type["type"] !== null ? input_type["type"] : type,
        "class": className,
        // "": className ? 'className: ' + className : el.tagName ? 'tagName: ' + el.tagName : '-' ,
        "resource-id": el_id
    };
}

function check_child_tag_name (el) {
    var input_type = {"input_type": null, "type": null, "checked": null};
    var childNodes = el.childNodes;
    var childNodesCnt = el.childElementCount;
    if (childNodesCnt > 0) {
        for (var i=0; i < childNodesCnt; i++) {
            if (childNodes[i].tagName && childNodes[i].tagName.toUpperCase() === "INPUT") {
                var check_input_result = check_input(childNodes[i]);
                input_type["input_type"] = check_input_result["input_type"];
                input_type["input_type"] = check_input_result["type"];
                input_type["checked"] = childNodes[i].checked ? childNodes[i].checked.toString() : "false";
                break;
            }
        }
    }
    return input_type;
}

function check_input(el) {
  var input_tag_check = el.tagName.toUpperCase() === "INPUT";
  var input_type;

  if ( input_tag_check && el.hasAttribute("type") ){
    var text_idx = input_type_text_list.indexOf(el.getAttribute("type"));
    if ( text_idx !== -1 ) {
      return {"input_type": input_type_text_list[text_idx], "type": "text"};
    }

    var click_idx = input_type_click_list.indexOf(el.getAttribute("type"));
    if ( click_idx !== -1 ) {
      return {"input_type": input_type_click_list[click_idx], "type": "click"};
    }

    var checkbox_idx = input_type_checkbox_list.indexOf(el.getAttribute("type"));
    if ( checkbox_idx !== -1 ) {
      return {"input_type": input_type_checkbox_list[checkbox_idx], "type": "checkbox"};
    }

    var etc_idx = input_type_etc_list.indexOf(el.getAttribute("type"));
    if ( etc_idx !== -1 ) {
      return {"input_type": input_type_etc_list[etc_idx], "type": "etc"};
    }
  }

  return {"input_type": null, "type": null };
}


var res_data = {
    "action_list": [],
    "window_width": 0,
    "window_height": 0,
    "current_url": "",
    "href": ""
};
var r_el = [];
var dom_el = [];
// Class명 : edittext, Action: input
var input_type_text_list = ["text", "search", "password", "textarea", "email", "number", "tel"];
// Class명 : button, action: click
var input_type_click_list = ["submit", "button", "reset"];
// Class명 ; view, action: checkbox|click
var input_type_checkbox_list = ["radio", "checkbox"];
// Class명 : spinner, action: spinner
var input_type_etc_list = ["date", "color", "datetime", "month", "range", "time", "week"];


var win_w = document.documentElement.clientWidth;
var win_h = document.documentElement.clientHeight;
var body = document.getElementsByTagName("body");
var els = body[0].getElementsByTagName("*");

if (window.$) {
    var at_jq = get_at_jq();
    var at_jq_keys = get_at_jq_keys(at_jq);
}

var t1 = Date.now();

for (var i = 0; i < els.length; i++) {
    var el_has_onclick = null;
    var el_has_onchange = null;
    var jQuery_has_events = undefined;
    var $_has_events = undefined;
    var point_el = null;
    var el = els[i];
    var el_id = els[i].id ? els[i].id : '';
    var el_h = el.getBoundingClientRect().height;
    var el_w = el.getBoundingClientRect().width;
    var x = el.getBoundingClientRect().left + (el_w / 2);
    var y = el.getBoundingClientRect().top + (el_h / 2);
    point_el = document.elementFromPoint(x, y);

    var size_check = el_h > 0 && el_h <= win_h && el_w > 0 && el_w <= win_w;

    var a_tag_check = el.tagName.toUpperCase() === "A";
    var href_check = el.hasAttribute('href') ? true : false;

    var select_tag_check = checkSelectChild(el);

    //////////////////////////// JQuery 검사를 통한 액션 추출 //////////////////////////////////
    var has_click_event_check = false;
    var has_change_event_check = false;

    if (at_jq_keys && at_jq_keys.length > 0) {
        for (var idx = 0; idx < at_jq_keys.length; idx++) {
            var version = at_jq[at_jq_keys[idx]].fn.jquery.split('.');
            //jQuery Version Check 1.8.0 기준
            if (version[0] < 2 && version[1] < 8) {
                jQuery_has_events = at_jq[at_jq_keys[idx]](el).data('events');
            } else {
                jQuery_has_events = at_jq[at_jq_keys[idx]]._data(el, "events");
            }

            // has Event Check (Click, Change)
            if (jQuery_has_events !== undefined && ('click' in jQuery_has_events)) {
                has_click_event_check = true;
            }
            if (jQuery_has_events !== undefined && ('change' in jQuery_has_events)) {
                has_change_event_check = true;
            }
        }
    }
    /////////////////////////////////////////////////////////////////////////////////////


    ////////////////////////// Get Event Listeners 를 통해 액션 추출//////////////////////////
    // var getEvL = getEventListeners(el);
    // has_click_event_check = 'click' in getEvL ? true : false;
    // has_change_event_check = 'change' in getEvL ? true : false;
    ///////////////////////////////////////////////////////////////////////////////////////

    el_has_onclick = el.hasAttribute("onclick") ? el.getAttribute("onclick") : null;
    el_has_onchange = el.hasAttribute("onchange") ? el.getAttribute("onchange") : null;

    var has_on_click_event_check = el_has_onclick !== null && el_has_onclick.length > 0;
    var has_on_change_event_check = el_has_onchange !== null && el_has_onchange.length > 0;

    var input_type = check_input(el);

    var is_equal_point_el = point_el === el;
    var is_contains_point_el = el.contains(point_el);
    var is_child_in_point_el = point_el && point_el.parentNode !== body[0] && el in point_el.parentNode.childNodes;
    var is_input_and_contains_in_point_el = el.tagName.toUpperCase() === "INPUT" && point_el && point_el.parentNode !== body[0] && point_el.parentNode.contains(el);

    var point_el_check = is_equal_point_el || is_contains_point_el || is_child_in_point_el || is_input_and_contains_in_point_el;

    // var point_el_check = point_el === el || el.contains(point_el) || (point_el && point_el.parentNode !== body[0] && point_el.parentNode.contains(el));


    // Action List Element & Dom Element List Save
    if (size_check && input_type.type === "text" && point_el_check) {
        var element_data = set_element_data(el, input_type.input_type, "input", 'WEBVIEW', 'input', el_id);
        check_interect_data_and_set_element(r_el, el, element_data);

        continue;
    }

    if (size_check && input_type.type === "checkbox" && point_el_check) {
        var element_data = set_element_data(el, input_type.input_type, "checkbox", 'WEBVIEW', 'view', el_id);
        check_interect_data_and_set_element(r_el, el, element_data);

        continue;
    }

    if (size_check && input_type.type === "etc" && point_el_check) {
        var element_data = set_element_data(el, input_type.input_type, "spinner", 'WEBVIEW', 'spinner', el_id);
        check_interect_data_and_set_element(r_el, el, element_data);

        continue;
    }

    if (size_check && select_tag_check && point_el_check) {
        var element_data = set_element_data(el, "null", "spinner", 'WEBVIEW', 'spinner', el_id);
        check_interect_data_and_set_element(r_el, el, element_data);

        continue;
    }

    if (size_check && select_tag_check && (has_click_event_check || has_on_click_event_check) && point_el_check) {
        var element_data = set_element_data(el, "null", "spinner", 'WEBVIEW', 'spinner', el_id);
        check_interect_data_and_set_element(r_el, el, element_data);

        continue;
    }

    if (size_check && ((a_tag_check && href_check) || href_check || has_click_event_check || has_on_click_event_check || input_type.type === "click") && point_el_check) {
        if (!equal_bounds_el_check(r_el, el)) {
            var element_data = set_element_data(el, "null", "click", 'WEBVIEW', 'button', el_id);
            check_interect_data_and_set_element(r_el, el, element_data);

            continue;
        } else {
            var zindex_check_result = zindex_check(r_el, el);
            if (zindex_check_result.result) {
                var f_el_idx = r_el.indexOf(zindex_check_result.f_el);
                r_el[f_el_idx] = set_element_data(el, "null", "click", 'WEBVIEW', 'button', el_id);
                continue;
            }
        }
    }

    if (size_check && (has_change_event_check || has_on_change_event_check) && point_el_check) {
        var element_data = set_element_data(el, "null", "spinner", 'WEBVIEW', 'spinner', el_id);
        check_interect_data_and_set_element(r_el, el, element_data);

        continue;
    }

    if (size_check && point_el_check) {
        dom_el.push(set_element_data(el, "null", "none", 'WEBVIEW', el.tagName, el_id));
        continue;
    }
}

res_data["current_url"] = window.location.hostname;
res_data["href"] = window.location.href;
res_data["window_width"] = win_w;
res_data["window_height"] = win_h;
res_data["action_list"] = r_el;
res_data["dom_list"] = dom_el;

return res_data;
