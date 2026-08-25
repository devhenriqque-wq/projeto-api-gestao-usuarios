const API = "";
const tokenKey = "jwt_gestao_usuarios";

const alerta = document.getElementById("alerta");
const telaLogin = document.getElementById("telaLogin");
const painel = document.getElementById("painel");
const btnLogout = document.getElementById("btnLogout");
const areaGestao = document.getElementById("areaGestao");
const areaCliente = document.getElementById("areaCliente");
const corpoTabela = document.getElementById("corpoTabela");
const formCard = document.getElementById("formCard");
const formUsuario = document.getElementById("formUsuario");
const perfilSelect = document.getElementById("perfil");
const btnNovo = document.getElementById("btnNovo");

let usuarioAtual = null;

function mostrarAlerta(mensagem, erro = false) {
  alerta.textContent = mensagem;
  alerta.classList.remove("oculto", "erro");
  if (erro) alerta.classList.add("erro");

  setTimeout(() => alerta.classList.add("oculto"), 3500);
}

function token() {
  return localStorage.getItem(tokenKey);
}

async function apiFetch(url, options = {}) {
  const headers = {
    "Content-Type": "application/json",
    ...(options.headers || {}),
  };

  if (token()) {
    headers.Authorization = `Bearer ${token()}`;
  }

  const response = await fetch(`${API}${url}`, {
    ...options,
    headers,
  });

  if (response.status === 204) return null;

  let data = null;
  try {
    data = await response.json();
  } catch (_) {
    data = {};
  }

  if (!response.ok) {
    const mensagem = data.detail || "Não foi possível concluir a operação.";
    throw new Error(mensagem);
  }

  return data;
}

async function entrar(email, senha) {
  const data = await apiFetch("/login", {
    method: "POST",
    body: JSON.stringify({ email, senha }),
  });

  localStorage.setItem(tokenKey, data.access_token);
  usuarioAtual = data.usuario;
  abrirPainel();
}

async function carregarAtual() {
  if (!token()) return false;

  try {
    usuarioAtual = await apiFetch("/me");
    abrirPainel();
    return true;
  } catch (_) {
    localStorage.removeItem(tokenKey);
    return false;
  }
}

function abrirPainel() {
  telaLogin.classList.add("oculto");
  painel.classList.remove("oculto");
  btnLogout.classList.remove("oculto");

  document.getElementById("nomeAtual").textContent = usuarioAtual.nome;
  document.getElementById("perfilAtual").textContent = usuarioAtual.perfil;

  if (usuarioAtual.perfil === "Cliente") {
    areaGestao.classList.add("oculto");
    areaCliente.classList.remove("oculto");

    document.getElementById("dadosCliente").innerHTML = `
      <div class="dado"><strong>ID</strong><span>${usuarioAtual.id}</span></div>
      <div class="dado"><strong>Nome</strong><span>${usuarioAtual.nome}</span></div>
      <div class="dado"><strong>E-mail</strong><span>${usuarioAtual.email}</span></div>
      <div class="dado"><strong>Perfil</strong><span>${usuarioAtual.perfil}</span></div>
    `;
  } else {
    areaCliente.classList.add("oculto");
    areaGestao.classList.remove("oculto");

    btnNovo.classList.toggle(
      "oculto",
      usuarioAtual.perfil !== "Administrador"
    );

    carregarUsuarios();
  }
}

async function carregarUsuarios() {
  try {
    const usuarios = await apiFetch("/usuarios");
    corpoTabela.innerHTML = "";

    usuarios.forEach((u) => {
      const tr = document.createElement("tr");

      const podeExcluir =
        usuarioAtual.perfil === "Administrador" &&
        usuarioAtual.id !== u.id;

      tr.innerHTML = `
        <td>${u.id}</td>
        <td>${u.nome}</td>
        <td>${u.email}</td>
        <td>${u.perfil}</td>
        <td>
          <div class="acoes-tabela">
            <button class="btn btn-editar" onclick="editarUsuario(${u.id})">
              Editar
            </button>
            ${
              podeExcluir
                ? `<button class="btn btn-perigo" onclick="excluirUsuario(${u.id})">Excluir</button>`
                : ""
            }
          </div>
        </td>
      `;

      corpoTabela.appendChild(tr);
    });
  } catch (erro) {
    mostrarAlerta(erro.message, true);
  }
}

window.editarUsuario = async function (id) {
  try {
    const u = await apiFetch(`/usuarios/${id}`);

    document.getElementById("usuarioId").value = u.id;
    document.getElementById("nome").value = u.nome;
    document.getElementById("email").value = u.email;
    document.getElementById("senha").value = "";
    perfilSelect.value = u.perfil;

    document.getElementById("tituloForm").textContent = "Editar usuário";
    document.getElementById("ajudaSenha").textContent =
      "Deixe em branco para manter a senha atual.";

    perfilSelect.disabled = usuarioAtual.perfil !== "Administrador";
    formCard.classList.remove("oculto");
  } catch (erro) {
    mostrarAlerta(erro.message, true);
  }
};

window.excluirUsuario = async function (id) {
  if (!confirm("Deseja realmente excluir este usuário?")) return;

  try {
    await apiFetch(`/usuarios/${id}`, { method: "DELETE" });
    mostrarAlerta("Usuário excluído com sucesso.");
    carregarUsuarios();
  } catch (erro) {
    mostrarAlerta(erro.message, true);
  }
};

document.getElementById("formLogin").addEventListener("submit", async (e) => {
  e.preventDefault();

  try {
    await entrar(
      document.getElementById("loginEmail").value,
      document.getElementById("loginSenha").value
    );
  } catch (erro) {
    mostrarAlerta(erro.message, true);
  }
});

btnLogout.addEventListener("click", () => {
  localStorage.removeItem(tokenKey);
  usuarioAtual = null;
  location.reload();
});

btnNovo.addEventListener("click", () => {
  formUsuario.reset();
  document.getElementById("usuarioId").value = "";
  document.getElementById("tituloForm").textContent = "Cadastrar usuário";
  document.getElementById("ajudaSenha").textContent =
    "Mínimo de 8 caracteres.";
  perfilSelect.disabled = false;
  formCard.classList.remove("oculto");
});

document.getElementById("btnCancelar").addEventListener("click", () => {
  formCard.classList.add("oculto");
});

formUsuario.addEventListener("submit", async (e) => {
  e.preventDefault();

  const id = document.getElementById("usuarioId").value;
  const nome = document.getElementById("nome").value;
  const email = document.getElementById("email").value;
  const senha = document.getElementById("senha").value;
  const perfil = perfilSelect.value;

  const payload = { nome, email };

  if (senha) payload.senha = senha;

  if (usuarioAtual.perfil === "Administrador") {
    payload.perfil = perfil;
  }

  try {
    if (id) {
      await apiFetch(`/usuarios/${id}`, {
        method: "PUT",
        body: JSON.stringify(payload),
      });
      mostrarAlerta("Usuário atualizado com sucesso.");
    } else {
      if (!senha) {
        throw new Error("Informe uma senha para o novo usuário.");
      }

      await apiFetch("/usuarios", {
        method: "POST",
        body: JSON.stringify({
          nome,
          email,
          senha,
          perfil,
        }),
      });
      mostrarAlerta("Usuário cadastrado com sucesso.");
    }

    formCard.classList.add("oculto");
    carregarUsuarios();
  } catch (erro) {
    mostrarAlerta(erro.message, true);
  }
});

carregarAtual();
