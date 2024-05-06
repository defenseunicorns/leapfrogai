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
  <path d="M31,29.36H1c-0.128,0-0.248-0.069-0.312-0.181c-0.064-0.111-0.064-0.248,0-0.359l15-26	c0.129-0.224,0.495-0.224,0.624,0l15,26c0.064,0.111,0.064,0.248,0,0.359S31.129,29.36,31,29.36z M1.624,28.64h28.753L16,3.72	L1.624,28.64z M16.36,20h-0.72V10h0.72V20z M16,23c-0.552,0-1,0.448-1,1s0.448,1,1,1s1-0.448,1-1S16.552,23,16,23z"></path>
</svg>