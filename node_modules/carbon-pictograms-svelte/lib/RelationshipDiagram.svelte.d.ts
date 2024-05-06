import type { SvelteComponentTyped } from "svelte";
import type { SvelteHTMLElements } from "svelte/elements";

type RestProps = SvelteHTMLElements["svg"];

export interface RelationshipDiagramProps extends RestProps {
  /**
   * Specify the pictogram title.
   * @default undefined
   */
  title?: string;

  [key: `data-${string}`]: any;
}

export default class RelationshipDiagram extends SvelteComponentTyped<
  RelationshipDiagramProps,
  Record<string, any>,
  {}
> {}
