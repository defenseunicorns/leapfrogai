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
  <path d="M30,29.36H2c-0.199,0-0.36-0.161-0.36-0.36v-4c0-0.199,0.161-0.36,0.36-0.36h28	c0.199,0,0.36,0.161,0.36,0.36v4C30.36,29.199,30.199,29.36,30,29.36z M2.36,28.64h27.28v-3.28H2.36V28.64z M14,23.36H2v-0.72h12	V23.36z M30,19.36H2c-0.199,0-0.36-0.161-0.36-0.36v-4c0-0.199,0.161-0.36,0.36-0.36h28c0.199,0,0.36,0.161,0.36,0.36v4	C30.36,19.199,30.199,19.36,30,19.36z M2.36,18.64h27.28v-3.28H2.36V18.64z M14,13.36H2v-0.72h12V13.36z M30,9.36H2	C1.801,9.36,1.64,9.199,1.64,9V5c0-0.199,0.161-0.36,0.36-0.36h28c0.199,0,0.36,0.161,0.36,0.36v4C30.36,9.199,30.199,9.36,30,9.36z M2.36,8.64h27.28V5.36H2.36V8.64z M14,3.36H2V2.64h12V3.36z"></path>
</svg>