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
  <path d="M28,31.36H4c-0.199,0-0.36-0.161-0.36-0.36V14.36H3c-0.199,0-0.36-0.161-0.36-0.36V8	c0-0.199,0.161-0.36,0.36-0.36h7.257C9.279,6.939,8.64,5.792,8.64,4.5c0-2.128,1.731-3.86,3.86-3.86c1.547,0,2.885,0.915,3.5,2.232	c0.615-1.317,1.953-2.232,3.5-2.232c2.128,0,3.86,1.731,3.86,3.86c0,1.292-0.64,2.439-1.617,3.14H29c0.199,0,0.36,0.161,0.36,0.36v6	c0,0.199-0.161,0.36-0.36,0.36h-0.64V31C28.36,31.199,28.199,31.36,28,31.36z M16.36,30.64h11.28V14.36H16.36V30.64z M4.36,30.64	h11.28V14.36H4.36V30.64z M16.36,13.64h12.28V8.36H16.36V13.64z M3.36,13.64h12.28V8.36H3.36V13.64z M16.36,7.64h3.14	c1.731,0,3.14-1.409,3.14-3.14s-1.408-3.14-3.14-3.14s-3.14,1.409-3.14,3.14V7.64z M12.5,7.64h3.14V4.5	c0-1.731-1.409-3.14-3.14-3.14S9.36,2.769,9.36,4.5S10.769,7.64,12.5,7.64z"></path>
</svg>