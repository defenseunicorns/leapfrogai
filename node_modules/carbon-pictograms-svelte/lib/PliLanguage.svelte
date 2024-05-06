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
  <path d="M3.899,16.999V7.222h3.895c1.751,0,2.731,1.079,2.731,2.802s-0.98,2.802-2.731,2.802H5.076V17	L3.899,16.999L3.899,16.999z M5.076,11.788h2.718c0.924,0,1.471-0.504,1.471-1.4V9.659c0-0.896-0.547-1.4-1.471-1.4H5.076V11.788z M12.382,16.999V7.222h1.177v8.741h4.161v1.036H12.382z M18.569,19.114l3.656-12.48h1.009l-3.656,12.48H18.569z M24.646,16.999	v-0.98h1.372V8.202h-1.372v-0.98h3.922v0.98h-1.373v7.816h1.373v0.98h-3.922V16.999z M31,30.64H1v0.721h30V30.64z M31,24.36H1	c-0.199,0-0.36-0.161-0.36-0.36V1c0-0.199,0.161-0.36,0.36-0.36h30c0.199,0,0.36,0.161,0.36,0.36v23	C31.36,24.199,31.199,24.36,31,24.36z M1.36,23.64h29.28V1.36H1.36V23.64z"></path>
</svg>