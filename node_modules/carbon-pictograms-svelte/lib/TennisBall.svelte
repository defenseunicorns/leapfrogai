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
  <path d="M22,0.64c-5.161,0-9.36,4.199-9.36,9.36	s4.199,9.36,9.36,9.36s9.36-4.199,9.36-9.36S27.161,0.64,22,0.64z M30.619,9.601c-4.369-0.416-7.805-3.852-8.221-8.221	C26.844,1.584,30.415,5.156,30.619,9.601z M13.38,10.399c4.369,0.416,7.805,3.852,8.221,8.221	C17.156,18.415,13.584,14.844,13.38,10.399z M22.324,18.623c-0.419-4.771-4.175-8.528-8.948-8.947c0.168-4.505,3.795-8.131,8.3-8.3	c0.419,4.771,4.175,8.529,8.947,8.948C30.455,14.829,26.829,18.455,22.324,18.623z M2.254,20.255l-0.509-0.51l8-8l0.509,0.509	L2.254,20.255z M19.745,21.745l0.51,0.51l-4,4l-0.509-0.51L19.745,21.745z M12.746,18.745l0.509,0.51l-12,12l-0.509-0.51	L12.746,18.745z"></path>
</svg>