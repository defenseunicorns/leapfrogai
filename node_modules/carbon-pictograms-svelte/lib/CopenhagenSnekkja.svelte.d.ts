import type { SvelteComponentTyped } from "svelte";
import type { SvelteHTMLElements } from "svelte/elements";

type RestProps = SvelteHTMLElements["svg"];

export interface CopenhagenSnekkjaProps extends RestProps {
  /**
   * Specify the pictogram title.
   * @default undefined
   */
  title?: string;

  [key: `data-${string}`]: any;
}

export default class CopenhagenSnekkja extends SvelteComponentTyped<
  CopenhagenSnekkjaProps,
  Record<string, any>,
  {}
> {}
