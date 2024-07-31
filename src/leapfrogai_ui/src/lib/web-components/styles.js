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
  .alternative {
      color: #111827;
      background-color: white;
      border: #e5e7eb;
      hover:bg-gray-100 dark:bg-gray-800 dark:text-gray-400 hover:text-primary-700 focus-within:text-primary-700 dark:focus-within:text-white dark:hover:text-white dark:hover:bg-gray-700
  }
`;
