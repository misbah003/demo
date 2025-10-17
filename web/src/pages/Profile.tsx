import { useState, useRef, useEffect } from "react";
import { ArrowLeft, Edit, Camera, Save, X, Sun, Moon, Upload, User, Mail, Phone, MapPin, Building, Briefcase, Calendar, ChevronDown, Shield, Bell } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover";
import { Calendar as CalendarComponent } from "@/components/ui/calendar";
import { format } from "date-fns";
import { useNavigate } from "react-router-dom";
import { useToast } from "@/hooks/use-toast";
import { useTheme } from "next-themes";
import { cn } from "@/lib/utils";
import { supabase } from "@/integrations/supabase/client";

const Profile = () => {
  const navigate = useNavigate();
  const { toast } = useToast();
  const { theme, setTheme } = useTheme();
  const [isEditing, setIsEditing] = useState(false);
  const [profileImage, setProfileImage] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);
  
  const [profileData, setProfileData] = useState({
    name: "John Doe",
    email: "john.doe@company.com",
    phone: "+1 (555) 123-4567",
    department: "Finance & Tax",
    position: "Senior Tax Analyst",
    location: "United States",
    joinDate: new Date("2022-01-15")
  });

  const [editData, setEditData] = useState(profileData);

  // Load profile data from database
  useEffect(() => {
    loadProfile();
  }, []);

  const loadProfile = async () => {
    try {
      const { data: { user } } = await supabase.auth.getUser();
      if (!user) {
        navigate('/auth');
        return;
      }

      const { data: profile, error } = await supabase
        .from('profiles')
        .select('*')
        .eq('user_id', user.id)
        .single();

      if (error && error.code !== 'PGRST116') { // PGRST116 = no rows returned
        throw error;
      }

      if (profile) {
        const loadedData = {
          name: profile.full_name || user.email || "User",
          email: profile.email || user.email || "",
          phone: profile.phone || "",
          department: profile.department || "Finance & Tax",
          position: profile.position || "Tax Analyst",
          location: profile.location || "United States",
          joinDate: profile.join_date ? new Date(profile.join_date) : new Date()
        };
        setProfileData(loadedData);
        setEditData(loadedData);
        setProfileImage(profile.avatar_url || null);
      }
    } catch (error) {
      console.error('Error loading profile:', error);
      toast({
        title: "Error Loading Profile",
        description: "Could not load your profile data.",
        variant: "destructive"
      });
    } finally {
      setLoading(false);
    }
  };

  // Dropdown options
  const countries = [
    "United States", "Canada", "United Kingdom", "Germany", "France", "Italy", "Spain", "Netherlands", 
    "Australia", "Japan", "South Korea", "Singapore", "India", "Brazil", "Mexico", "Argentina",
    "Switzerland", "Sweden", "Norway", "Denmark", "Finland", "Austria", "Belgium", "Ireland"
  ];

  const departments = [
    "Finance & Tax", "Accounting", "Human Resources", "Information Technology", "Marketing", 
    "Sales", "Operations", "Legal", "Research & Development", "Customer Service", "Administration",
    "Business Development", "Quality Assurance", "Supply Chain", "Executive"
  ];

  const positions = [
    "Senior Tax Analyst", "Tax Manager", "Tax Director", "Accountant", "Senior Accountant", 
    "Financial Analyst", "Controller", "CFO", "Manager", "Senior Manager", "Director", 
    "Vice President", "Analyst", "Specialist", "Coordinator", "Associate", "Executive"
  ];

  const handleSave = async () => {
    setSaving(true);
    try {
      const { data: { user } } = await supabase.auth.getUser();
      if (!user) {
        throw new Error('Not authenticated');
      }

      // Update profile in database
      const { error } = await supabase
        .from('profiles')
        .upsert({
          user_id: user.id,
          email: editData.email,
          full_name: editData.name,
          phone: editData.phone,
          department: editData.department,
          position: editData.position,
          location: editData.location,
          join_date: format(editData.joinDate, 'yyyy-MM-dd'),
          avatar_url: profileImage,
          updated_at: new Date().toISOString()
        }, {
          onConflict: 'user_id'
        });

      if (error) throw error;

      setProfileData(editData);
      setIsEditing(false);
      toast({
        title: "Profile Updated",
        description: "Your profile information has been saved successfully."
      });
    } catch (error) {
      console.error('Error saving profile:', error);
      toast({
        title: "Save Failed",
        description: error instanceof Error ? error.message : "Could not save profile",
        variant: "destructive"
      });
    } finally {
      setSaving(false);
    }
  };

  const handleCancel = () => {
    setEditData(profileData);
    setIsEditing(false);
  };

  const handleImageUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      // Validate file size (max 5MB)
      if (file.size > 5 * 1024 * 1024) {
        toast({
          title: "File Too Large",
          description: "Please select an image smaller than 5MB.",
          variant: "destructive"
        });
        return;
      }

      // Validate file type
      if (!file.type.startsWith('image/')) {
        toast({
          title: "Invalid File Type",
          description: "Please select an image file (JPG, PNG, GIF, etc.).",
          variant: "destructive"
        });
        return;
      }

      try {
        const { data: { user } } = await supabase.auth.getUser();
        if (!user) throw new Error('Please log in to upload a profile photo');

        // Show loading toast
        toast({
          title: "Uploading...",
          description: "Please wait while we upload your photo."
        });

        // Upload to Supabase Storage
        const fileExt = file.name.split('.').pop();
        const fileName = `${user.id}-${Date.now()}.${fileExt}`;
        const filePath = `avatars/${fileName}`;

        const { error: uploadError } = await supabase.storage
          .from('documents')
          .upload(filePath, file, { 
            upsert: true,
            contentType: file.type
          });

        if (uploadError) {
          console.error('Upload error:', uploadError);
          throw new Error(`Upload failed: ${uploadError.message}`);
        }

        // Get public URL
        const { data: { publicUrl } } = supabase.storage
          .from('documents')
          .getPublicUrl(filePath);

        setProfileImage(publicUrl);

        // Update profile with new avatar URL (upsert to create if doesn't exist)
        const { error: updateError } = await supabase
          .from('profiles')
          .upsert({
            user_id: user.id,
            avatar_url: publicUrl,
            updated_at: new Date().toISOString()
          }, {
            onConflict: 'user_id'
          });

        if (updateError) {
          console.error('Update error:', updateError);
          throw new Error(`Failed to update profile: ${updateError.message}`);
        }

        toast({
          title: "Photo Updated",
          description: "Your profile photo has been updated successfully."
        });
      } catch (error) {
        console.error('Error uploading image:', error);
        toast({
          title: "Upload Failed",
          description: error instanceof Error ? error.message : "Could not upload profile photo. Please try again.",
          variant: "destructive"
        });
      }
    }
  };

  const triggerFileInput = () => {
    fileInputRef.current?.click();
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-background via-background to-muted/20">
      {/* Header */}
      <header className="bg-card/80 backdrop-blur-xl border-b border-border/50 px-6 py-6 shadow-elegant">
        <div className="flex items-center justify-between max-w-7xl mx-auto">
          <div className="flex items-center space-x-6">
            <Button 
              variant="ghost" 
              size="icon"
              onClick={() => navigate("/")}
              className="hover:bg-primary/10 hover:text-primary transition-smooth"
            >
              <ArrowLeft className="h-5 w-5" />
            </Button>
            <div>
              <h1 className="text-2xl font-bold text-foreground bg-gradient-primary bg-clip-text text-transparent">
                Profile Settings
              </h1>
              <p className="text-sm text-muted-foreground mt-1">Manage your account information and preferences</p>
            </div>
          </div>
          
          <div className="flex items-center space-x-3">
            <Button 
              variant="ghost" 
              size="icon"
              onClick={() => setTheme(theme === "dark" ? "light" : "dark")}
              className="hover:bg-primary/10 hover:text-primary transition-smooth"
            >
              {theme === "dark" ? <Sun className="h-5 w-5" /> : <Moon className="h-5 w-5" />}
            </Button>
            
            {isEditing ? (
              <>
                <Button variant="outline" size="sm" onClick={handleCancel} disabled={saving} className="hover:bg-destructive/10 hover:text-destructive hover:border-destructive/50 transition-smooth">
                  <X className="h-4 w-4 mr-2" />
                  Cancel
                </Button>
                <Button size="sm" onClick={handleSave} disabled={saving} className="bg-gradient-primary hover:shadow-glow transition-smooth">
                  <Save className="h-4 w-4 mr-2" />
                  {saving ? "Saving..." : "Save Changes"}
                </Button>
              </>
            ) : (
              <Button size="sm" onClick={() => setIsEditing(true)} className="bg-gradient-primary hover:shadow-glow transition-smooth">
                <Edit className="h-4 w-4 mr-2" />
                Edit Profile
              </Button>
            )}
          </div>
        </div>
      </header>

      <input
        type="file"
        ref={fileInputRef}
        onChange={handleImageUpload}
        accept="image/*"
        className="hidden"
      />

      {/* Content */}
      <main className="px-6 py-8 max-w-7xl mx-auto">
        <div className="grid grid-cols-1 xl:grid-cols-4 gap-8">
          {/* Profile Card */}
          <div className="xl:col-span-1">
            <Card className="shadow-card border-border/50 bg-gradient-card backdrop-blur-sm hover:shadow-glow transition-smooth">
              <CardContent className="p-8 text-center">
                <div className="relative mx-auto mb-8 group">
                  <div className="relative">
                    <Avatar className="h-32 w-32 mx-auto ring-4 ring-primary/20 transition-smooth hover:ring-primary/40">
                      <AvatarImage 
                        src={profileImage || "/placeholder.svg"} 
                        alt="Profile" 
                        className="object-cover"
                      />
                      <AvatarFallback className="text-3xl bg-gradient-primary text-primary-foreground">
                        {profileData.name.split(' ').map(n => n[0]).join('')}
                      </AvatarFallback>
                    </Avatar>
                    {isEditing && (
                      <div className="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 transition-smooth rounded-full flex items-center justify-center cursor-pointer" onClick={triggerFileInput}>
                        <Upload className="h-8 w-8 text-white" />
                      </div>
                    )}
                  </div>
                  {isEditing && (
                    <Button 
                      size="icon" 
                      onClick={triggerFileInput}
                      className="absolute -bottom-2 -right-2 h-10 w-10 rounded-full bg-gradient-primary hover:shadow-glow transition-smooth"
                    >
                      <Camera className="h-5 w-5" />
                    </Button>
                  )}
                </div>
                
                <div className="space-y-3">
                  <h2 className="text-2xl font-bold text-foreground break-words px-2">
                    {profileData.name.length > 30 ? profileData.name.substring(0, 30) + '...' : profileData.name}
                  </h2>
                  <div className="inline-flex items-center px-3 py-1 rounded-full bg-primary/10 text-primary text-sm font-medium max-w-full">
                    <Briefcase className="h-4 w-4 mr-2 flex-shrink-0" />
                    <span className="truncate">{profileData.position}</span>
                  </div>
                  <div className="flex items-center justify-center text-muted-foreground text-sm px-2">
                    <Building className="h-4 w-4 mr-2 flex-shrink-0" />
                    <span className="truncate">{profileData.department}</span>
                  </div>
                  <div className="flex items-center justify-center text-muted-foreground text-sm">
                    <Calendar className="h-4 w-4 mr-2 flex-shrink-0" />
                    Joined {format(profileData.joinDate, "MMMM yyyy")}
                  </div>
                </div>
              </CardContent>
            </Card>
            
            {/* Quick Stats */}
            <Card className="mt-6 shadow-card border-border/50 bg-gradient-card backdrop-blur-sm">
              <CardContent className="p-6">
                <h3 className="font-semibold text-foreground mb-4">Quick Stats</h3>
                <div className="space-y-3">
                  <div className="flex justify-between text-sm">
                    <span className="text-muted-foreground">Profile Complete</span>
                    <span className="font-medium text-success">95%</span>
                  </div>
                  <div className="w-full bg-muted rounded-full h-2">
                    <div className="bg-gradient-success h-2 rounded-full" style={{ width: '95%' }}></div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Information Cards */}
          <div className="xl:col-span-3 space-y-6">
            {/* Personal Information */}
            <Card className="shadow-card border-border/50 bg-gradient-card backdrop-blur-sm hover:shadow-elegant transition-smooth">
              <CardHeader className="pb-4">
                <div className="flex items-center space-x-3">
                  <div className="p-2 rounded-lg bg-primary/10">
                    <User className="h-5 w-5 text-primary" />
                  </div>
                  <CardTitle className="text-xl font-semibold text-foreground">
                    Personal Information
                  </CardTitle>
                </div>
              </CardHeader>
              <CardContent className="space-y-6">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div className="space-y-3">
                    <Label htmlFor="name" className="text-sm font-medium text-foreground flex items-center">
                      <User className="h-4 w-4 mr-2 text-muted-foreground" />
                      Full Name
                    </Label>
                    {isEditing ? (
                      <Input
                        id="name"
                        value={editData.name}
                        onChange={(e) => setEditData({...editData, name: e.target.value})}
                        maxLength={50}
                        className="transition-smooth focus:ring-primary/20 focus:border-primary"
                        placeholder="Enter your full name (max 50 characters)"
                      />
                    ) : (
                      <div className="text-sm text-foreground bg-muted/50 rounded-lg px-4 py-3 border border-border/50 break-words">
                        {profileData.name}
                      </div>
                    )}
                  </div>
                  
                  <div className="space-y-3">
                    <Label htmlFor="email" className="text-sm font-medium text-foreground flex items-center">
                      <Mail className="h-4 w-4 mr-2 text-muted-foreground" />
                      Email Address
                    </Label>
                    {isEditing ? (
                      <Input
                        id="email"
                        type="email"
                        value={editData.email}
                        onChange={(e) => setEditData({...editData, email: e.target.value})}
                        className="transition-smooth focus:ring-primary/20 focus:border-primary"
                      />
                    ) : (
                      <div className="text-sm text-foreground bg-muted/50 rounded-lg px-4 py-3 border border-border/50">
                        {profileData.email}
                      </div>
                    )}
                  </div>
                  
                  <div className="space-y-3">
                    <Label htmlFor="phone" className="text-sm font-medium text-foreground flex items-center">
                      <Phone className="h-4 w-4 mr-2 text-muted-foreground" />
                      Phone Number
                    </Label>
                    {isEditing ? (
                      <Input
                        id="phone"
                        value={editData.phone}
                        onChange={(e) => setEditData({...editData, phone: e.target.value})}
                        className="transition-smooth focus:ring-primary/20 focus:border-primary"
                      />
                    ) : (
                      <div className="text-sm text-foreground bg-muted/50 rounded-lg px-4 py-3 border border-border/50">
                        {profileData.phone}
                      </div>
                    )}
                  </div>
                  
                  <div className="space-y-3">
                    <Label htmlFor="location" className="text-sm font-medium text-foreground flex items-center">
                      <MapPin className="h-4 w-4 mr-2 text-muted-foreground" />
                      Country
                    </Label>
                    {isEditing ? (
                      <Select value={editData.location} onValueChange={(value) => setEditData({...editData, location: value})}>
                        <SelectTrigger className="transition-smooth focus:ring-primary/20 focus:border-primary">
                          <SelectValue placeholder="Select country" />
                        </SelectTrigger>
                        <SelectContent className="bg-popover border-border shadow-elegant max-h-60">
                          {countries.map((country) => (
                            <SelectItem key={country} value={country} className="hover:bg-accent/50">
                              {country}
                            </SelectItem>
                          ))}
                        </SelectContent>
                      </Select>
                    ) : (
                      <div className="text-sm text-foreground bg-muted/50 rounded-lg px-4 py-3 border border-border/50">
                        {profileData.location}
                      </div>
                    )}
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Work Information */}
            <Card className="shadow-card border-border/50 bg-gradient-card backdrop-blur-sm hover:shadow-elegant transition-smooth">
              <CardHeader className="pb-4">
                <div className="flex items-center space-x-3">
                  <div className="p-2 rounded-lg bg-intelligence-blue/10">
                    <Briefcase className="h-5 w-5 text-intelligence-blue" />
                  </div>
                  <CardTitle className="text-xl font-semibold text-foreground">
                    Work Information
                  </CardTitle>
                </div>
              </CardHeader>
              <CardContent className="space-y-6">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div className="space-y-3">
                    <Label htmlFor="position" className="text-sm font-medium text-foreground flex items-center">
                      <Briefcase className="h-4 w-4 mr-2 text-muted-foreground" />
                      Position
                    </Label>
                    {isEditing ? (
                      <Select value={editData.position} onValueChange={(value) => setEditData({...editData, position: value})}>
                        <SelectTrigger className="transition-smooth focus:ring-primary/20 focus:border-primary">
                          <SelectValue placeholder="Select position" />
                        </SelectTrigger>
                        <SelectContent className="bg-popover border-border shadow-elegant max-h-60">
                          {positions.map((position) => (
                            <SelectItem key={position} value={position} className="hover:bg-accent/50">
                              {position}
                            </SelectItem>
                          ))}
                        </SelectContent>
                      </Select>
                    ) : (
                      <div className="text-sm text-foreground bg-muted/50 rounded-lg px-4 py-3 border border-border/50">
                        {profileData.position}
                      </div>
                    )}
                  </div>
                  
                  <div className="space-y-3">
                    <Label htmlFor="department" className="text-sm font-medium text-foreground flex items-center">
                      <Building className="h-4 w-4 mr-2 text-muted-foreground" />
                      Department
                    </Label>
                    {isEditing ? (
                      <Select value={editData.department} onValueChange={(value) => setEditData({...editData, department: value})}>
                        <SelectTrigger className="transition-smooth focus:ring-primary/20 focus:border-primary">
                          <SelectValue placeholder="Select department" />
                        </SelectTrigger>
                        <SelectContent className="bg-popover border-border shadow-elegant max-h-60">
                          {departments.map((department) => (
                            <SelectItem key={department} value={department} className="hover:bg-accent/50">
                              {department}
                            </SelectItem>
                          ))}
                        </SelectContent>
                      </Select>
                    ) : (
                      <div className="text-sm text-foreground bg-muted/50 rounded-lg px-4 py-3 border border-border/50">
                        {profileData.department}
                      </div>
                    )}
                  </div>
                  
                  <div className="space-y-3">
                    <Label htmlFor="joinDate" className="text-sm font-medium text-foreground flex items-center">
                      <Calendar className="h-4 w-4 mr-2 text-muted-foreground" />
                      Join Date
                    </Label>
                    {isEditing ? (
                      <Popover>
                        <PopoverTrigger asChild>
                          <Button
                            variant="outline"
                            className={cn(
                              "w-full justify-start text-left font-normal transition-smooth focus:ring-primary/20 focus:border-primary",
                              !editData.joinDate && "text-muted-foreground"
                            )}
                          >
                            <Calendar className="mr-2 h-4 w-4" />
                            {editData.joinDate ? format(editData.joinDate, "PPP") : <span>Pick a date</span>}
                          </Button>
                        </PopoverTrigger>
                        <PopoverContent className="w-auto p-0 bg-popover border-border shadow-elegant" align="start">
                          <CalendarComponent
                            mode="single"
                            selected={editData.joinDate}
                            onSelect={(date) => date && setEditData({...editData, joinDate: date})}
                            disabled={(date) =>
                              date > new Date() || date < new Date("1900-01-01")
                            }
                            initialFocus
                            className={cn("p-3 pointer-events-auto")}
                          />
                        </PopoverContent>
                      </Popover>
                    ) : (
                      <div className="text-sm text-foreground bg-muted/50 rounded-lg px-4 py-3 border border-border/50">
                        {format(profileData.joinDate, "PPP")}
                      </div>
                    )}
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Privacy & Security Settings */}
            <Card className="shadow-card border-border/50 bg-gradient-card backdrop-blur-sm hover:shadow-elegant transition-smooth">
              <CardHeader className="pb-4">
                <div className="flex items-center space-x-3">
                  <div className="p-2 rounded-lg bg-destructive/10">
                    <Shield className="h-5 w-5 text-destructive" />
                  </div>
                  <CardTitle className="text-xl font-semibold text-foreground">
                    Privacy & Security
                  </CardTitle>
                </div>
              </CardHeader>
              <CardContent className="space-y-6">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div className="space-y-4">
                    <div className="flex items-center justify-between p-4 border border-border/50 rounded-lg bg-muted/30">
                      <div>
                        <h4 className="text-sm font-medium text-foreground">Two-Factor Authentication</h4>
                        <p className="text-xs text-muted-foreground">Add an extra layer of security</p>
                      </div>
                      <Button variant="outline" size="sm">
                        Enable
                      </Button>
                    </div>
                    <div className="flex items-center justify-between p-4 border border-border/50 rounded-lg bg-muted/30">
                      <div>
                        <h4 className="text-sm font-medium text-foreground">Login Notifications</h4>
                        <p className="text-xs text-muted-foreground">Get notified of new sign-ins</p>
                      </div>
                      <Button variant="outline" size="sm">
                        Enabled
                      </Button>
                    </div>
                  </div>
                  <div className="space-y-4">
                    <div className="flex items-center justify-between p-4 border border-border/50 rounded-lg bg-muted/30">
                      <div>
                        <h4 className="text-sm font-medium text-foreground">Data Export</h4>
                        <p className="text-xs text-muted-foreground">Download your data</p>
                      </div>
                      <Button variant="outline" size="sm">
                        Export
                      </Button>
                    </div>
                    <div className="flex items-center justify-between p-4 border border-border/50 rounded-lg bg-muted/30">
                      <div>
                        <h4 className="text-sm font-medium text-foreground">Change Password</h4>
                        <p className="text-xs text-muted-foreground">Update your password</p>
                      </div>
                      <Button variant="outline" size="sm">
                        Change
                      </Button>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Notification Preferences */}
            <Card className="shadow-card border-border/50 bg-gradient-card backdrop-blur-sm hover:shadow-elegant transition-smooth">
              <CardHeader className="pb-4">
                <div className="flex items-center space-x-3">
                  <div className="p-2 rounded-lg bg-warning/10">
                    <Bell className="h-5 w-5 text-warning" />
                  </div>
                  <CardTitle className="text-xl font-semibold text-foreground">
                    Notification Preferences
                  </CardTitle>
                </div>
              </CardHeader>
              <CardContent className="space-y-6">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div className="space-y-4">
                    <div className="flex items-center justify-between p-4 border border-border/50 rounded-lg bg-muted/30">
                      <div>
                        <h4 className="text-sm font-medium text-foreground">Email Notifications</h4>
                        <p className="text-xs text-muted-foreground">Receive updates via email</p>
                      </div>
                      <Button variant="secondary" size="sm">
                        Enabled
                      </Button>
                    </div>
                    <div className="flex items-center justify-between p-4 border border-border/50 rounded-lg bg-muted/30">
                      <div>
                        <h4 className="text-sm font-medium text-foreground">Tax Alerts</h4>
                        <p className="text-xs text-muted-foreground">Important tax deadline reminders</p>
                      </div>
                      <Button variant="secondary" size="sm">
                        Enabled
                      </Button>
                    </div>
                  </div>
                  <div className="space-y-4">
                    <div className="flex items-center justify-between p-4 border border-border/50 rounded-lg bg-muted/30">
                      <div>
                        <h4 className="text-sm font-medium text-foreground">System Updates</h4>
                        <p className="text-xs text-muted-foreground">New features and maintenance</p>
                      </div>
                      <Button variant="outline" size="sm">
                        Disabled
                      </Button>
                    </div>
                    <div className="flex items-center justify-between p-4 border border-border/50 rounded-lg bg-muted/30">
                      <div>
                        <h4 className="text-sm font-medium text-foreground">Weekly Reports</h4>
                        <p className="text-xs text-muted-foreground">Analytics summary emails</p>
                      </div>
                      <Button variant="secondary" size="sm">
                        Enabled
                      </Button>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </main>
    </div>
  );
};

export default Profile;