import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { Button } from '../components/ui/button';
import { Input } from '../components/ui/input';
import { Label } from '../components/ui/label';
import { toast } from 'sonner';
import { Map } from 'lucide-react';

const Login = () => {
  const [isLogin, setIsLogin] = useState(true);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [fullName, setFullName] = useState('');
  const [loading, setLoading] = useState(false);
  const { login, register } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      if (isLogin) {
        await login(email, password);
        toast.success('Login successful');
      } else {
        await register(email, password, fullName);
        toast.success('Registration successful');
      }
      navigate('/dashboard');
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Authentication failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex">
      {/* Left side - Form */}
      <div className="w-full lg:w-1/2 flex items-center justify-center p-8 bg-zinc-950">
        <div className="w-full max-w-md space-y-8">
          <div className="text-center">
            <div className="inline-flex items-center justify-center w-16 h-16 rounded-sm bg-primary/10 border border-primary/20 mb-4">
              <Map className="w-8 h-8 text-primary" />
            </div>
            <h1 className="text-4xl font-black tracking-tight text-white" style={{ fontFamily: 'Chivo, sans-serif' }}>
              AutoMapGuard
            </h1>
            <p className="mt-2 text-zinc-400">
              AI-Driven Urban Change Detection System
            </p>
          </div>

          <form onSubmit={handleSubmit} className="mt-8 space-y-6" data-testid="auth-form">
            <div className="space-y-4">
              {!isLogin && (
                <div>
                  <Label htmlFor="fullName" className="text-zinc-300">Full Name</Label>
                  <Input
                    id="fullName"
                    type="text"
                    value={fullName}
                    onChange={(e) => setFullName(e.target.value)}
                    required={!isLogin}
                    className="mt-1 bg-zinc-900 border-zinc-800 text-white"
                    data-testid="fullname-input"
                  />
                </div>
              )}
              <div>
                <Label htmlFor="email" className="text-zinc-300">Email</Label>
                <Input
                  id="email"
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                  className="mt-1 bg-zinc-900 border-zinc-800 text-white"
                  data-testid="email-input"
                />
              </div>
              <div>
                <Label htmlFor="password" className="text-zinc-300">Password</Label>
                <Input
                  id="password"
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                  className="mt-1 bg-zinc-900 border-zinc-800 text-white"
                  data-testid="password-input"
                />
              </div>
            </div>

            <Button
              type="submit"
              className="w-full"
              disabled={loading}
              data-testid="auth-submit-button"
            >
              {loading ? 'Processing...' : (isLogin ? 'Sign In' : 'Sign Up')}
            </Button>

            <div className="text-center">
              <button
                type="button"
                onClick={() => setIsLogin(!isLogin)}
                className="text-sm text-primary hover:text-primary/80 transition-colors"
                data-testid="toggle-auth-mode"
              >
                {isLogin ? "Don't have an account? Sign up" : 'Already have an account? Sign in'}
              </button>
            </div>
          </form>
        </div>
      </div>

      {/* Right side - Background */}
      <div 
        className="hidden lg:block lg:w-1/2 bg-cover bg-center relative"
        style={{
          backgroundImage: 'url(https://images.unsplash.com/photo-1636451734006-31bb356f163d?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDQ2NDN8MHwxfHNlYXJjaHwyfHxtb2Rlcm4lMjBjaXR5JTIwc2t5bGluZSUyMGJsdWUlMjBob3VyfGVufDB8fHx8MTc2ODQ3NDk1NHww&ixlib=rb-4.1.0&q=85)'
        }}
      >
        <div className="absolute inset-0 bg-zinc-950/60 backdrop-blur-sm" />
        <div className="relative h-full flex items-center justify-center p-12">
          <div className="text-center max-w-lg">
            <h2 className="text-5xl font-black text-white mb-6" style={{ fontFamily: 'Chivo, sans-serif' }}>
              Map the Future
            </h2>
            <p className="text-xl text-zinc-300">
              Professional geospatial change detection with enterprise-grade geometry compliance
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Login;
