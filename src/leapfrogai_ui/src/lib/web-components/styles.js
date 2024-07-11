import { css } from 'lit';

// These styles are copied from highlight.js/styles/atom-one-dark-reasonable.css
// for use in the CodeBlock web component
export const highlightJsStyles = css`
  pre code.hljs {
    display: block;
    overflow-x: auto;
    padding: 1em;
  }
  code.hljs {
    padding: 3px 5px;
  }
  /*

Atom One Dark With support for ReasonML by Gidi Morris, based off work by Daniel Gamage

Original One Dark Syntax theme from https://github.com/atom/one-dark-syntax

*/
  .hljs {
    color: #abb2bf;
    background: #282c34;
  }
  .hljs-keyword,
  .hljs-operator {
    color: #f92672;
  }
  .hljs-pattern-match {
    color: #f92672;
  }
  .hljs-pattern-match .hljs-constructor {
    color: #61aeee;
  }
  .hljs-function {
    color: #61aeee;
  }
  .hljs-function .hljs-params {
    color: #a6e22e;
  }
  .hljs-function .hljs-params .hljs-typing {
    color: #fd971f;
  }
  .hljs-module-access .hljs-module {
    color: #7e57c2;
  }
  .hljs-constructor {
    color: #e2b93d;
  }
  .hljs-constructor .hljs-string {
    color: #9ccc65;
  }
  .hljs-comment,
  .hljs-quote {
    color: #b18eb1;
    font-style: italic;
  }
  .hljs-doctag,
  .hljs-formula {
    color: #c678dd;
  }
  .hljs-section,
  .hljs-name,
  .hljs-selector-tag,
  .hljs-deletion,
  .hljs-subst {
    color: #e06c75;
  }
  .hljs-literal {
    color: #56b6c2;
  }
  .hljs-string,
  .hljs-regexp,
  .hljs-addition,
  .hljs-attribute,
  .hljs-meta .hljs-string {
    color: #98c379;
  }
  .hljs-built_in,
  .hljs-title.class_,
  .hljs-class .hljs-title {
    color: #e6c07b;
  }
  .hljs-attr,
  .hljs-variable,
  .hljs-template-variable,
  .hljs-type,
  .hljs-selector-class,
  .hljs-selector-attr,
  .hljs-selector-pseudo,
  .hljs-number {
    color: #d19a66;
  }
  .hljs-symbol,
  .hljs-bullet,
  .hljs-link,
  .hljs-meta,
  .hljs-selector-id,
  .hljs-title {
    color: #61aeee;
  }
  .hljs-emphasis {
    font-style: italic;
  }
  .hljs-strong {
    font-weight: bold;
  }
  .hljs-link {
    text-decoration: underline;
  }
`;

// Styles copied from carbon for use in CodeBlock web component
export const buttonStyles = css`
  .bx--btn {
    font-size: 0.875rem;
    font-weight: 400;
    line-height: 1.28572;
    letter-spacing: 0.16px;
    position: relative;
    display: inline-flex;
    max-width: 20rem;
    min-height: 3rem;
    flex-shrink: 0;
    align-items: center;
    justify-content: space-between;
    padding: calc(0.875rem - 3px) 63px calc(0.875rem - 3px) 15px;
    margin: 0;
    border-radius: 0;
    cursor: pointer;
    outline: none;
    text-align: left;
    text-decoration: none;
    transition:
      background 70ms cubic-bezier(0, 0, 0.38, 0.9),
      box-shadow 70ms cubic-bezier(0, 0, 0.38, 0.9),
      border-color 70ms cubic-bezier(0, 0, 0.38, 0.9),
      outline 70ms cubic-bezier(0, 0, 0.38, 0.9);
    vertical-align: top;
  }

  .bx--btn--tertiary {
    border-width: 1px;
    border-style: solid;
    border-color: #fff;
    background-color: #0000;
    color: #fff;
  }

  .bx--btn--tertiary:focus {
    background-color: #fff;
    color: #161616;
    border-color: #fff;
    box-shadow:
      inset 0 0 0 1px #fff,
      inset 0 0 0 2px #262626;
  }

  .bx--btn--tertiary:hover {
    background-color: #f4f4f4;
    color: #000000;
  }

  .bx--btn--sm {
    min-height: 2rem;
    padding: calc(0.375rem - 3px) 60px calc(0.375rem - 3px) 12px;
  }

  .bx--btn__icon {
    position: absolute;
    right: 1rem;
    width: 1rem;
    height: 1rem;
    flex-shrink: 0;
  }
`;
