(() => {
  const menu = document.querySelector(".farama-header-menu__body");
  if (!menu || menu.dataset.faramaMenuLoading) return;
  menu.dataset.faramaMenuLoading = "true";

  const imageBase = "https://farama.org/assets/images";
  const foundationLinks = [
    { name: "About", website: "https://farama.org/about" },
    { name: "Standards", website: "https://farama.org/project_standards" },
    { name: "Donate", website: "https://farama.org/donations" },
  ];

  function projectList(projects, showLogos) {
    const list = document.createElement("ul");
    list.className = "farama-header-menu-list";

    for (const project of projects) {
      const item = document.createElement("li");
      const link = document.createElement("a");
      link.href = project.website ?? project.github;

      if (showLogos) {
        const logo = document.createElement("img");
        logo.src = imageBase + (project.image || "/farama_black.svg");
        logo.alt = "";
        logo.className = "farama-black-logo-invert";
        link.append(logo);
      }

      link.append(project.name);
      item.append(link);
      list.append(item);
    }

    return list;
  }

  function section(title, className = "section") {
    const element = document.createElement("div");
    element.className = `farama-header-menu__${className}`;
    const heading = document.createElement("span");
    heading.className = `farama-header-menu__${className}-title`;
    heading.textContent = title;
    element.append(heading);
    return element;
  }

  function group(title, lists) {
    const element = section(title);
    const columns = document.createElement("div");
    columns.className = "farama-header-menu__subsections-container";
    columns.style.display = "flex";

    for (const [name, projects] of Object.entries(lists)) {
      const column = section(name, "subsection");
      column.append(projectList(projects, true));
      columns.append(column);
    }

    element.append(columns);
    return element;
  }

  function renderProjects(projects) {
    const core = [];
    const mature = [];
    const incubatingDocs = [];
    const incubatingRepos = [];
    for (const project of projects) {
      if (project.type === "core") {
        core.push(project);
      } else if (project.type === "mature") {
        if (project.website != null) mature.push(project);
      } else if (project.website != null) {
        incubatingDocs.push(project);
      } else {
        incubatingRepos.push(project);
      }
    }

    const coreSection = section("Core Projects");
    coreSection.append(projectList(core, true));
    const foundation = section("Foundation");
    foundation.append(projectList(foundationLinks, true));
    const stack = document.createElement("div");
    stack.style.cssText = "display: flex; flex-direction: column";
    stack.append(coreSection, foundation);

    menu.replaceChildren(
      stack,
      group("Mature Projects", { Documentation: mature }),
      group("Incubating Projects", { Documentation: incubatingDocs, Repositories: incubatingRepos }),
    );
  }

  fetch("https://farama.org/api/projects.json")
    .then((response) => {
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      return response.json();
    })
    .then(renderProjects)
    .catch((error) => {
      delete menu.dataset.faramaMenuLoading;
      console.warn("Unable to load Farama projects", error);
    });
})();
