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
  <path d="M5,21.36H1c-0.199,0-0.36-0.161-0.36-0.36V5c0-0.199,0.161-0.36,0.36-0.36h30	c0.144,0,0.273,0.085,0.331,0.217c0.057,0.132,0.029,0.285-0.069,0.39l-8.5,9l-0.523-0.494l7.927-8.393H1.36v15.28H5V21.36z M29.36,28v-5c0-0.199-0.161-0.36-0.36-0.36H7c-0.199,0-0.36,0.161-0.36,0.36v5c0,0.199,0.161,0.36,0.36,0.36h22	C29.199,28.36,29.36,28.199,29.36,28z M7.36,23.36h21.28v4.279H7.36V23.36z M27,24.64h-6v0.721h6V24.64z M10,24.64H9v0.721h1V24.64z M12,24.64h-1v0.721h1V24.64z M14,24.64h-1v0.721h1V24.64z M29.36,21v-5c0-0.199-0.161-0.36-0.36-0.36H7	c-0.199,0-0.36,0.161-0.36,0.36v5c0,0.199,0.161,0.36,0.36,0.36h22C29.199,21.36,29.36,21.199,29.36,21z M7.36,16.36h21.28v4.28	H7.36V16.36z M27,17.64h-6v0.721h6V17.64z M10,17.64H9v0.721h1V17.64z M12,17.64h-1v0.721h1V17.64z M14,17.64h-1v0.721h1V17.64z"></path>
</svg>