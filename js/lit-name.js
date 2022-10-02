import {LitElement, html} from '../node_modules/lit';
import {asyncReplace} from '../node_modules/lit/directives/async-replace.js';

const realName = "Steven Broaddus";

// Very inefficient function that I wrote very quickly
async function* randomizeName(myName) {
  let index = 0;
  let charIndex = 0;   
  let randomChars = ["!", "$", "%", "^", "&", "*", "(", ")", "+", "=", "-", "/", "\\", "[", "]", "{", "}"];
  for (let i = 0; i < 25; i++) { 
      index = Math.floor(Math.random() * myName.length);
      charIndex = Math.floor(Math.random() * randomChars.length);
      if (/\S/.test(myName.charAt(index))) {
       yield myName = myName.substring(0, index) + randomChars[charIndex] + myName.substring(index + randomChars[charIndex].length);
      } else {
       yield myName;
      }
      await new Promise((r) => setTimeout(r, 25)); 
  }
  for (let i = 0; i < myName.length; i++) {
    if (randomChars.includes(myName.charAt(i))){
      yield myName = myName.substring(0, i) + realName.charAt(i) + myName.substring(i + 1);
    }
    await new Promise((r) => setTimeout(r, 25));
  }
}

class nameElement extends LitElement {
    static properties = {
      myName: {state: true},
    };
  
    constructor() {
      super();
      this.myName = randomizeName(realName);
    }
  
    render() {
      return html`<span>${asyncReplace(this.myName)}</span>`;
    }
  }
  customElements.define('lit-name', nameElement);