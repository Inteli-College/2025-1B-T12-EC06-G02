---
sidebar_position: 1
custom_edit_url: null
---

# Banco de dados

<p style={{textAlign: 'center'}}>Figura 1: Estrutura do banco de dados</p>
<div style={{margin: 25}}>
    <div style={{textAlign: 'center'}}>
        <img src={require("../../../../static/img/database/database.png").default} style={{width: 800}} alt="Tela de login" />
        <br />
    </div>
</div>
<p style={{textAlign: 'center'}}>Fonte: Produzida pelos Autores (2025). </p>

[Link para o D2](https://play.d2lang.com/?script=zFbBbtswDL3rKwj0nB_wYUC3XXYYMLTY2WBsxmEjS55Ib3WL_PtgKVacpsjcIRt6MkTSJB_fo-wb-IyKaxSC-2pLLcLGB_gUsNrBrUM7CAvcD6LUGnMD34UCfEWHDbXk1PRCQQp4NgCyxY4KkB-2VFxbMgBcF9D3XMNz5Z1oQHZaQBe4xTCUOxr2BsBhSwUoPaoBoBbZ5lPw9uiqAqFSXaIWoNySKLYd_GLdxiM8eTfW7Lt6SZhF0dL6ht2FsP0I-VvwD1TpHHWXTJeBCwVGuxx6TVIF7pS9yzas60Ai_2QG-4nP1YTwVsRXjGMHkdjyWjhjstfFsPGBuHFT5KFiDGan1FC4EB8hfGmxoTk7PBrebc8AG7ZUdqjbTGu0nIhBh-54EH6icrfO2UdhPPJRFRvrfcinvrMe6z-LpCXFGhULeBDv1mmYeeXvSHqrYkJ6_r9pauhFcc2WdZgjFvpJ4YXtZEqLdmO-0asDxhPdT2ReCXdKs1gafyH_O-p8iETF5_uV_RtHcb4lDTkKCylOU1mlu2HO72FM5XUuiZRtMaZY9G3k2ti2bLmT9LGF1Qd4cTlvUaBFN-Tv0qWYnGSaQLov5OTlyVd5p8huVjrvxcRGviJG79n2rMl61wioP8l_FnfeXtbzsdA8Q3bnFmdtZCe7yvY11cCZ-Zk_iyBXT4bXQuaZzA3cqw_YkJH0TDqqxr-m_MbHvtqRxt-p6DgMNavmNCSLe_KavfkdAAD__w%3D%3D&sketch=0&theme=0&)

```sql
-- Tabela de usuários (integrada com autenticação Supabase)
CREATE TABLE users (
  id UUID PRIMARY KEY REFERENCES auth.users(id),
  name TEXT,
  email TEXT,
  role TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  last_login TIMESTAMP WITH TIME ZONE
);

-- Tabela de projetos
CREATE TABLE projects (
  id SERIAL PRIMARY KEY,
  name TEXT,
  description TEXT,
  address TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Tabela de relação usuários-projetos
CREATE TABLE user_projects (
  id SERIAL PRIMARY KEY,
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  project_id INTEGER REFERENCES projects(id) ON DELETE CASCADE
);

-- Tabela de imagens
CREATE TABLE images (
  id SERIAL PRIMARY KEY,
  user_id UUID REFERENCES users(id) ON DELETE SET NULL,
  project_id INTEGER REFERENCES projects(id) ON DELETE CASCADE,
  file_path TEXT,
  file_name TEXT,
  type TEXT,
  axis TEXT,
  floor TEXT,
  size_kb INTEGER,
  uploaded_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  metadata JSONB
);

-- Tabela de resultados (análises de IA)
CREATE TABLE results (
  id SERIAL PRIMARY KEY,
  user_id UUID REFERENCES users(id) ON DELETE SET NULL,
  trustability INTEGER,
  severity INTEGER,
  type TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Tabela de relação projeto-resultados
CREATE TABLE project_results (
  id SERIAL PRIMARY KEY,
  result_id INTEGER REFERENCES results(id) ON DELETE CASCADE,
  project_id INTEGER REFERENCES projects(id) ON DELETE CASCADE
);

-- Tabela de relatórios
CREATE TABLE reports (
  id SERIAL PRIMARY KEY,
  user_id UUID REFERENCES users(id) ON DELETE SET NULL,
  project_id INTEGER REFERENCES projects(id) ON DELETE CASCADE,
  result_id INTEGER REFERENCES results(id) ON DELETE SET NULL,
  file_path TEXT,
  generated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Tabela de relação relatórios-imagens
CREATE TABLE reports_images (
  id SERIAL PRIMARY KEY,
  report_id INTEGER REFERENCES reports(id) ON DELETE CASCADE,
  image_id INTEGER REFERENCES images(id) ON DELETE CASCADE
);

-- Trigger para sincronizar usuários do auth.users com a tabela users personalizada
CREATE OR REPLACE FUNCTION public.handle_new_user() 
RETURNS TRIGGER AS $$
BEGIN
  INSERT INTO public.users (id, email, name, created_at)
  VALUES (new.id, new.email, new.raw_user_meta_data->>'name', new.created_at);
  RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

CREATE TRIGGER on_auth_user_created
  AFTER INSERT ON auth.users
  FOR EACH ROW EXECUTE FUNCTION public.handle_new_user();

-- Função para atualizar timestamps
CREATE OR REPLACE FUNCTION update_modified_column()
RETURNS TRIGGER AS $$
BEGIN
   NEW.updated_at = NOW();
   RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_users_modtime
BEFORE UPDATE ON users
FOR EACH ROW EXECUTE PROCEDURE update_modified_column();

CREATE TRIGGER update_projects_modtime
BEFORE UPDATE ON projects
FOR EACH ROW EXECUTE PROCEDURE update_modified_column();

-- Criar buckets para armazenamento
INSERT INTO storage.buckets (id, name, public)
VALUES 
  ('crack_images', 'Imagens de Fissuras', false),
  ('reports', 'Relatórios', false)
ON CONFLICT DO NOTHING;

-- Habilitar RLS em todas as tabelas
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE projects ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_projects ENABLE ROW LEVEL SECURITY;
ALTER TABLE images ENABLE ROW LEVEL SECURITY;
ALTER TABLE results ENABLE ROW LEVEL SECURITY;
ALTER TABLE project_results ENABLE ROW LEVEL SECURITY;
ALTER TABLE reports ENABLE ROW LEVEL SECURITY;
ALTER TABLE reports_images ENABLE ROW LEVEL SECURITY;

-- Políticas para usuários
CREATE POLICY "Usuários podem ver seu próprio perfil" ON users
  FOR SELECT USING (auth.uid() = id);
  
CREATE POLICY "Usuários podem atualizar seu próprio perfil" ON users
  FOR UPDATE USING (auth.uid() = id);

-- Políticas para projetos
CREATE POLICY "Usuários podem ver seus projetos" ON projects
  FOR SELECT USING (
    id IN (
      SELECT project_id FROM user_projects WHERE user_id = auth.uid()
    )
  );

CREATE POLICY "Usuários podem editar seus projetos" ON projects
  FOR UPDATE USING (
    id IN (
      SELECT project_id FROM user_projects WHERE user_id = auth.uid()
    )
  );

CREATE POLICY "Usuários podem inserir projetos" ON projects
  FOR INSERT WITH CHECK (true);

-- Políticas para user_projects
CREATE POLICY "Usuários podem ver suas associações projeto-usuário" ON user_projects
  FOR SELECT USING (user_id = auth.uid());

CREATE POLICY "Usuários podem criar associações projeto-usuário" ON user_projects
  FOR INSERT WITH CHECK (user_id = auth.uid());

-- Políticas para imagens
CREATE POLICY "Usuários podem ver imagens de seus projetos" ON images
  FOR SELECT USING (
    project_id IN (
      SELECT project_id FROM user_projects WHERE user_id = auth.uid()
    )
  );

CREATE POLICY "Usuários podem inserir imagens em seus projetos" ON images
  FOR INSERT WITH CHECK (
    project_id IN (
      SELECT project_id FROM user_projects WHERE user_id = auth.uid()
    )
  );

-- Políticas para resultados
CREATE POLICY "Usuários podem ver resultados" ON results
  FOR SELECT USING (
    id IN (
      SELECT result_id FROM project_results WHERE project_id IN (
        SELECT project_id FROM user_projects WHERE user_id = auth.uid()
      )
    ) OR user_id = auth.uid()
  );

-- Políticas para relatórios
CREATE POLICY "Usuários podem ver seus relatórios" ON reports
  FOR SELECT USING (
    project_id IN (
      SELECT project_id FROM user_projects WHERE user_id = auth.uid()
    ) OR user_id = auth.uid()
  );

-- Políticas para storage (versão corrigida sem usar storage.fspath)
CREATE POLICY "Acesso de usuários às suas imagens" ON storage.objects
  FOR SELECT USING (
    bucket_id = 'crack_images' AND 
    (auth.uid() IS NOT NULL) AND
    (position(auth.uid()::text in name) > 0)
  );

CREATE POLICY "Upload de imagens pelos usuários" ON storage.objects
  FOR INSERT WITH CHECK (
    bucket_id = 'crack_images' AND 
    (auth.uid() IS NOT NULL) AND
    (position(auth.uid()::text in name) > 0)
  );

CREATE POLICY "Acesso de usuários aos seus relatórios" ON storage.objects
  FOR SELECT USING (
    bucket_id = 'reports' AND 
    (auth.uid() IS NOT NULL) AND
    (position(auth.uid()::text in name) > 0)
  );

-- Índices para melhorar performance
CREATE INDEX idx_user_projects_user ON user_projects(user_id);
CREATE INDEX idx_user_projects_project ON user_projects(project_id);
CREATE INDEX idx_images_project ON images(project_id);
CREATE INDEX idx_reports_project ON reports(project_id);
CREATE INDEX idx_reports_result ON reports(result_id);
CREATE INDEX idx_project_results_project ON project_results(project_id);
```