import { LitElement, css, html } from 'lit';
import { unsafeHTML } from 'lit/directives/unsafe-html.js';
import DOMPurify from 'isomorphic-dompurify';
import { highlightJsStyles, buttonStyles } from './styles.js';
import { toastStore } from '$stores';

/*
  The markdown-it highlight option used in Message.svelte does not allow us to insert normal Svelte components in the
  <pre><code>... block that it returns. This Web Component is instead used within that
  function to properly render the code blocks with highlighting and a copy button.
  Attempts to use svelte's customElements to compile a Svelte component into a Web Component caused
  Flash of Unstyled Content (FUOC) issues so we built the component from scratch instead.
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
      button {
        display: flex;
        justify-content: center;
        align-items: center;
      }
    `
  ];

  constructor() {
    super();
    this.code = '';
    this.language = '';
  }

  static get properties() {
    return {
      code: {
        type: String,
        reflect: true
      },
      language: {
        type: String,
        reflect: true
      }
    };
  }

  removeHtml = () => {
    const tmp = document.createElement('DIV');
    tmp.innerHTML = DOMPurify.sanitize(this.code);
    return tmp.textContent || tmp.innerText || '';
  };

  handleClick = async () => {
    await navigator.clipboard.writeText(this.removeHtml());
    toastStore.addToast({
      kind: 'info',
      title: 'Code Copied'
    });
  };

  render() {
    const { code, language } = this;
    return html`
      <div class="code-block">
        <div class="code-block-header">
          <span>${language}</span>
          <div class="centered-flexbox">
            <button
              id="copy-btn"
              data-testid="copy-code-btn"
              @click=${this.handleClick}
              class="copy-btn-base dark"
            >
              <span>Copy</span>
              <svg
                aria-hidden="true"
                xmlns="http://www.w3.org/2000/svg"
                width="24"
                height="24"
                fill="none"
                viewBox="0 0 24 24"
              >
                <path
                  stroke="currentColor"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M9 8v3a1 1 0 0 1-1 1H5m11 4h2a1 1 0 0 0 1-1V5a1 1 0 0 0-1-1h-7a1 1 0 0 0-1 1v1m4 3v10a1 1 0 0 1-1 1H6a1 1 0 0 1-1-1v-7.13a1 1 0 0 1 .24-.65L7.7 8.35A1 1 0 0 1 8.46 8H13a1 1 0 0 1 1 1Z"
                />
              </svg>
            </button>
          </div>
        </div>
        <div class="code-block-inner">${unsafeHTML(DOMPurify.sanitize(code))}</div>
      </div>
    `;
  }
}

customElements.get('code-block') || customElements.define('code-block', CodeBlock);
