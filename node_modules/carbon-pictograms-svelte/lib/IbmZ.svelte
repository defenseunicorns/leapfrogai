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
  <path d="M28,31.36H4c-0.199,0-0.36-0.161-0.36-0.36v-6c0-0.09,0.034-0.177,0.095-0.243L19.682,7.36H4	C3.801,7.36,3.64,7.199,3.64,7V1c0-0.199,0.161-0.36,0.36-0.36h24c0.199,0,0.36,0.161,0.36,0.36v6c0,0.09-0.034,0.177-0.095,0.243	L12.318,24.64H28c0.199,0,0.36,0.161,0.36,0.36v6C28.36,31.199,28.199,31.36,28,31.36z M9.083,30.64h16.875L11.68,25.449	L9.083,30.64z M4.36,30.64h3.42l-3.42-4.56V30.64z M13.543,25.36l14.096,5.126V25.36H13.543z M4.467,25.023l3.971,5.295l10.59-21.18	L4.467,25.023z M23.562,1.682l-10.59,21.18L27.533,6.977L23.562,1.682z M4.36,6.64h14.097L4.36,1.514V6.64z M6.043,1.36	l14.278,5.192l2.597-5.192C22.918,1.36,6.043,1.36,6.043,1.36z M24.22,1.36l3.42,4.56V1.36H24.22z"></path>
</svg>