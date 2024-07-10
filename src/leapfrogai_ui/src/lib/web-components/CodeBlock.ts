import { LitElement, css, html } from 'lit';
import DOMPurify from 'dompurify';
import { highlightJsStyles, buttonStyles } from './styles.js';
import { unsafeHTML } from 'lit-html/directives/unsafe-html.js';
import { toastStore } from '$stores';

/*
  The markdown-it highlight option used in Message.svelte does not allow us to insert normal Svelte components in the
  <pre><code>... block that it returns. This Web Component is instead used within that
  function to properly render the code blocks with highlighting and a copy button.
 */
export class CodeBlock extends LitElement {
  static styles = [
    highlightJsStyles,
    buttonStyles,
    css`
      :host {
        display: flex;
      }
      .centered-flexbox {
        display: flex;
        justify-content: center;
        align-items: center;
      }

      .code-block {
        display: flex;
        flex-direction: column;
        width: 100%;
        background-color: #262626;
        border: 0.5px solid #525252;
        border-radius: 0.375rem;
        overflow: hidden;
      }
      .code-block-inner {
        overflow-x: auto;
        width: 100%;
        padding: 1rem;
        box-sizing: border-box;
      }
      .code-block-header {
        display: flex;
        align-items: center;
        background-color: rgba(141, 141, 141, 0.16);
        padding: 0.5rem 1rem;
        font-size: 0.75rem;
        justify-content: space-between;
        border-top-left-radius: 0.375rem;
        border-top-right-radius: 0.375rem;
      }
    `
  ];

  static get properties() {
    return {
      code: {
        type: String,
        reflect: true
      },
      lang: {
        type: String,
        reflect: true
      }
    };
  }

  constructor() {
    super();
    this.code = '';
    this.lang = '';
  }

  removeHtml = () => {
    const tmp = document.createElement('DIV');
    tmp.innerHTML = this.code;
    return tmp.textContent || tmp.innerText || '';
  };

  handleClick = async () => {
    await navigator.clipboard.writeText(this.removeHtml());
    toastStore.addToast({
      kind: 'info',
      title: 'Code Copied',
      subtitle: ''
    });
  };

  render() {
    const { code, lang } = this;
    return html`
      <div class="code-block">
        <div class="code-block-header">
          <span>${lang}</span>
          <div class="centered-flexbox">
            <button
              data-testid="code-copy-btn"
              class="bx--btn bx--btn--tertiary bx--btn--sm "
              @click=${this.handleClick}
            >
              <div style="display: flex; width: 100%;">
                <span>Copy</span>
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  viewBox="0 0 32 32"
                  fill="currentColor"
                  preserveAspectRatio="xMidYMid meet"
                  width="16"
                  height="16"
                  aria-hidden="true"
                  class="bx--btn__icon"
                >
                  <path
                    d="M28,10V28H10V10H28m0-2H10a2,2,0,0,0-2,2V28a2,2,0,0,0,2,2H28a2,2,0,0,0,2-2V10a2,2,0,0,0-2-2Z"
                  ></path>
                  <path d="M4,18H2V4A2,2,0,0,1,4,2H18V4H4Z"></path>
                </svg>
              </div>
            </button>
          </div>
        </div>
        <div class="code-block-inner">${unsafeHTML(DOMPurify.sanitize(code))}</div>
      </div>
    `;
  }
}

customElements.define('code-block', CodeBlock);
