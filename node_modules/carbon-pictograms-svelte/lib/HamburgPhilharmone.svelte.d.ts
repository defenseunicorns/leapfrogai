import type { SvelteComponentTyped } from "svelte";
import type { SvelteHTMLElements } from "svelte/elements";

type RestProps = SvelteHTMLElements["svg"];

export interface HamburgPhilharmoneProps extends RestProps {
  /**
   * Specify the pictogram title.
   * @default undefined
   */
  title?: string;

  [key: `data-${string}`]: any;
}

export default class HamburgPhilharmone extends SvelteComponentTyped<
  HamburgPhilharmoneProps,
  Record<string, any>,
  {}
> {}
