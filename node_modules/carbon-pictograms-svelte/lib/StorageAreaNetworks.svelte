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
  <path d="M16,29.36c-1.179,0-2.159-0.869-2.333-2H5v-0.72h8.667c0.156-1.014,0.959-1.816,1.973-1.973	V23.36H5c-0.199,0-0.36-0.161-0.36-0.36v-5c0-0.199,0.161-0.36,0.36-0.36h22c0.199,0,0.36,0.161,0.36,0.36v5	c0,0.199-0.161,0.36-0.36,0.36H16.36v1.307c1.014,0.156,1.817,0.959,1.973,1.973H27v0.721h-8.667	C18.159,28.491,17.179,29.36,16,29.36z M16,25.36c-0.904,0-1.64,0.735-1.64,1.64s0.736,1.64,1.64,1.64c0.904,0,1.64-0.735,1.64-1.64	S16.904,25.36,16,25.36z M5.36,22.64h21.28v-4.28H5.36V22.64z M25,20.36h-6v-0.72h6V20.36z M12,20.36h-1v-0.72h1V20.36z M10,20.36H9	v-0.72h1V20.36z M8,20.36H7v-0.72h1V20.36z M27,16.36H5c-0.199,0-0.36-0.161-0.36-0.36v-5c0-0.199,0.161-0.36,0.36-0.36h22	c0.199,0,0.36,0.161,0.36,0.36v5C27.36,16.199,27.199,16.36,27,16.36z M5.36,15.64h21.28v-4.28H5.36V15.64z M25,13.36h-6v-0.72h6	V13.36z M12,13.36h-1v-0.72h1V13.36z M10,13.36H9v-0.72h1V13.36z M8,13.36H7v-0.72h1V13.36z M27,9.36H5	C4.801,9.36,4.64,9.199,4.64,9V4c0-0.199,0.161-0.36,0.36-0.36h22c0.199,0,0.36,0.161,0.36,0.36v5C27.36,9.199,27.199,9.36,27,9.36z M5.36,8.64h21.28V4.36H5.36V8.64z M25,6.36h-6V5.64h6V6.36z M12,6.36h-1V5.64h1V6.36z M10,6.36H9V5.64h1V6.36z M8,6.36H7V5.64h1	V6.36z"></path>
</svg>