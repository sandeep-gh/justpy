import { init, getLocaleFromNavigator } from "svelte-i18n";
import App from "./App.svelte";
import Chart from "./Chart.svelte";
import Dummy from "./Dummy.svelte";
import "./Tailwind.svelte";
import "./i18n";

const fallbackLocale = "en-US";
const navigatorLocale = getLocaleFromNavigator();

init({
  fallbackLocale,
  initialLocale: ["en-US", "fr-FR"].includes(navigatorLocale)
    ? navigatorLocale
    : fallbackLocale,
});

// var justpyComponents = [{
//     "attrs": {},
//     "id": null,
//     "vue_type": "html_component",
//     "show": true,
//     "events": [],
//     "event_modifiers": {},
//     "classes": "bg-pink-100",
//     "style": "",
//     "set_focus": false,
//     "html_tag": "div",
//     "class_name": "Div",
//     "event_propagation": true,
//     "inner_html": "",
//     "animation": false,
//     "debug": false,
//     "transition": null,
//     "directives": {},
//     "scoped_slots": {},
//     "object_props": [{
//         "attrs": {
//             "id": "1"
//         },
//         "id": 1,
//         "vue_type": "html_component",
//         "show": true,
//         "events": ["click"],
//         "event_modifiers": {},
//         "classes": "",
//         "style": "color: blue; font-size: 30px",
//         "set_focus": false,
//         "html_tag": "button",
//         "class_name": "Button",
//         "event_propagation": true,
//         "inner_html": "",
//         "animation": false,
//         "debug": false,
//         "transition": null,
//         "directives": {},
//         "scoped_slots": {},
//         "object_props": [],
//         "text": "abtn"
//     }, {
//         "attrs": {},
//         "id": null,
//         "vue_type": "html_component",
//         "show": true,
//         "events": [],
//         "event_modifiers": {},
//         "classes": "",
//         "style": "color: blue; font-size: 30px",
//         "set_focus": false,
//         "html_tag": "button",
//         "class_name": "Button",
//         "event_propagation": true,
//         "inner_html": "",
//         "animation": false,
//         "debug": false,
//         "transition": null,
//         "directives": {},
//         "scoped_slots": {},
//         "object_props": [],
//         "text": "abtn2"
//     }],
//     "text": "outer dive"
// }];


// const app = new App({
//   target: document.body,
//   props: {
//       name: "world",
//     atag: "span",
//     justpyComponents : justpyComponents
//   },
// });

//export default App;
export {App, Chart};
