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

export const buttonStyles = css`
  .copy-btn-base {
    display: inline-flex;
    justify-content: center;
    align-items: center;
    border-radius: 0.5rem;
    border: 1px solid #e5e7eb;
    background-color: white;
    padding: 0.25rem 0.5rem;
    text-align: center;
    font-size: 0.875rem;
    line-height: 1.25rem;
    font-weight: 500;
    color: #111827;
    cursor: pointer;
  }

  .dark,
  copy-btn-base {
    background: transparent;
    color: #f3f4f6;
    border: 1px solid white;
  }

  .copy-btn-base:hover {
    color: #1d4ed8;
    background-color: #f3f4f6;
  }

  .dark:hover {
    background-color: #374151;
    color: white;
    border: 1px solid #4b5563;
  }
`;
