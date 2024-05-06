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
  <path d="M31,31.36H1c-0.199,0-0.36-0.161-0.36-0.36V1c0-0.199,0.161-0.36,0.36-0.36h30c0.199,0,0.36,0.161,0.36,0.36	v30C31.36,31.199,31.199,31.36,31,31.36z M1.36,30.64h29.28V9.869L17.255,23.255c-0.142,0.141-0.369,0.141-0.509,0L10,16.509	l-8.64,8.64C1.36,25.149,1.36,30.64,1.36,30.64z M1.36,9.36v14.771l8.386-8.385c0.141-0.141,0.368-0.141,0.509,0L17,22.491	L30.131,9.36H1.36z M1.36,8.64h29.28V1.36H1.36V8.64z"></path>
</svg>