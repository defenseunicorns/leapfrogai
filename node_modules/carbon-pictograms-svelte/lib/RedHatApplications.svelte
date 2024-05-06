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
  <path d="M28,28.36H12	c-0.199,0-0.36-0.161-0.36-0.36v-7.64H4c-0.199,0-0.36-0.161-0.36-0.36V5c0-0.199,0.161-0.36,0.36-0.36h16	c0.199,0,0.36,0.161,0.36,0.36v7.64H28c0.199,0,0.36,0.161,0.36,0.36v15C28.36,28.199,28.199,28.36,28,28.36z M12.36,27.64h15.28	V13.36H12.36V27.64z M4.36,19.64h7.28V13c0-0.199,0.161-0.36,0.36-0.36h7.639V5.36H4.36V19.64z M19,16.36h-4v-0.72h4V16.36z M11,8.36H7V7.64h4V8.36z"></path>
</svg>