<script>
  /**
   * Specify the pictogram title.
   * @type {string}
   */
  export let title = undefined;

  $: labelled =  $$props["aria-label"] || $$props["aria-labelledby"] || $$props["title"];
  $: attributes = {
    "aria-hidden": labelled ? undefined : true,
    role: labelled ? "img" : undefined,
    focusable: Number($$props["tabindex"]) === 0  ? true : undefined,
  };
</script>

<svg
  preserveAspectRatio="xMidYMid meet"
  xmlns="http://www.w3.org/2000/svg"
  viewBox="0 0 32 32"
  width="64"
  height="64"
  fill="currentColor"
  {title}
  {...attributes}
  {...$$restProps}>
  <path d="M28.811,26.812l-4.33-2.5l0.359-0.623l4.33,2.5L28.811,26.812z M31,19.36h-5v-0.72h5	V19.36z M16,19.36L1,19.355v-0.721l15,0.005V19.36z M24.84,14.312l-0.359-0.624l4.33-2.5l0.359,0.624L24.84,14.312z M7.16,14.312	l-4.33-2.5l0.36-0.624l4.33,2.5L7.16,14.312z M21.312,10.52l-0.623-0.36l2.5-4.33l0.623,0.36L21.312,10.52z M10.688,10.52l-2.5-4.33	l0.624-0.36l2.5,4.33L10.688,10.52z M16.36,9h-0.72V4h0.72V9z"></path>
</svg>